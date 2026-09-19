import hashlib
import json
import os
import re
import threading
from datetime import date, datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from util.taiwan_time import TaiwanTime


SOURCE_URL = "https://soldier.ntpc.gov.tw/mt6480"
TAIPEI_SOURCE_URL = (
    "https://docms.gov.taipei/News.aspx?"
    "n=27EEFB0FD3624B52&sms=98D477013A337FFF"
)
CACHE_TTL = timedelta(days=1)
CACHE_SCHEMA_VERSION = 5
TAIPEI_MAX_PDFS = max(1, int(os.getenv("TROOP_CALENDAR_TAIPEI_MAX_PDFS", "40")))
CACHE_PATH = Path(
    os.getenv(
        "TROOP_CALENDAR_CACHE_PATH",
        Path(__file__).resolve().parents[1] / "cache" / "troop_calendar.json",
    )
)

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; DeserterCalendar/1.0; "
        "+https://github.com/)"
    )
}

PRIMARY_SOURCE = {
    "id": "ntpc",
    "name": "新北市政府役男大亨 ONLINE",
    "url": SOURCE_URL,
    "role": "primary",
}
TAIPEI_SOURCE = {
    "id": "taipei",
    "name": "臺北市政府兵役局訓練流路 PDF",
    "url": TAIPEI_SOURCE_URL,
    "role": "supplementary",
}

_cache_lock = threading.Lock()
_roc_date_pattern = re.compile(r"(?P<year>\d{2,3})年\s*(?P<month>\d{1,2})月\s*(?P<day>\d{1,2})日")
_date_range_pattern = re.compile(
    r"(?:(?P<start_year>\d{2,3})年\s*)?"
    r"(?P<start_month>\d{1,2})月\s*(?P<start_day>\d{1,2})日?\s*"
    r"(?:-|－|–|—|~|～|至)\s*"
    r"(?:(?P<end_year>\d{2,3})年\s*)?"
    r"(?:(?P<end_month>\d{1,2})月\s*)?"
    r"(?P<end_day>\d{1,2})日"
)
_single_date_pattern = re.compile(
    r"(?:(?P<year>\d{2,3})年\s*)?"
    r"(?P<month>\d{1,2})月\s*(?P<day>\d{1,2})日"
)

_taipei_calendar_labels = (
    "海軍陸戰隊專長訓練",
    "專長訓練階段",
    "部隊訓練階段",
    "入伍結訓鑑測",
    "新訓結訓鑑測",
    "第一階段結訓",
    "游泳訓練日期",
    "專長甄選日期",
    "單位選填日期",
    "結訓日期",
    "退伍日期",
    "撥交日期",
    "游泳訓練",
    "游泳鑑測",
    "結訓鑑測",
    "專長甄選",
    "單位選填",
    "憲兵抽籤日",
    "懇親會客",
    "懇親日",
    "懇親",
    "休假日",
    "休假",
    "抽籤日",
    "抽籤",
    "撥交日",
    "撥交",
    "結訓",
    "退伍",
)


def _print_calendar_progress(message: str) -> None:
    print(
        f"{TaiwanTime.string(ms=True)} | [TroopCalendar] {message}",
        flush=True,
    )


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def strip_camp_from_title(title: str) -> str:
    """營區已有獨立欄位，梯次標題不重複保留尾端營區括號。"""
    return re.sub(r"\s*[（(][^）)]*營區[）)]\s*$", "", title).strip()


def _parse_roc_date(value: str) -> date | None:
    match = _roc_date_pattern.search(value)
    if not match:
        return None
    try:
        return date(
            int(match.group("year")) + 1911,
            int(match.group("month")),
            int(match.group("day")),
        )
    except ValueError:
        return None


def _resolve_event_date(
    year: str | None,
    month: int,
    day: int,
    enlistment_date: date,
    reference_date: date | None = None,
) -> date | None:
    try:
        if year:
            return date(int(year) + 1911, month, day)

        base_year = reference_date.year if reference_date else enlistment_date.year
        parsed = date(base_year, month, day)
        threshold = reference_date or (enlistment_date - timedelta(days=31))
        if parsed < threshold:
            parsed = date(base_year + 1, month, day)
        return parsed
    except ValueError:
        return None


def _extract_event_dates(value: str, enlistment_date: date) -> list[tuple[date, date]]:
    results: list[tuple[date, date]] = []
    occupied_spans: list[tuple[int, int]] = []

    for match in _date_range_pattern.finditer(value):
        start = _resolve_event_date(
            match.group("start_year"),
            int(match.group("start_month")),
            int(match.group("start_day")),
            enlistment_date,
        )
        if not start:
            continue

        end = _resolve_event_date(
            match.group("end_year"),
            int(match.group("end_month") or match.group("start_month")),
            int(match.group("end_day")),
            enlistment_date,
            reference_date=start,
        )
        if end:
            results.append((start, end))
            occupied_spans.append(match.span())

    for match in _single_date_pattern.finditer(value):
        if any(start <= match.start() < end for start, end in occupied_spans):
            continue
        parsed = _resolve_event_date(
            match.group("year"),
            int(match.group("month")),
            int(match.group("day")),
            enlistment_date,
        )
        if parsed:
            results.append((parsed, parsed))

    unique_results = []
    seen = set()
    for start, end in results:
        key = (start.isoformat(), end.isoformat())
        if key not in seen:
            seen.add(key)
            unique_results.append((start, end))
    return unique_results


def _normalize_branch(title: str) -> str:
    if "海軍陸戰隊" in title or "海陸" in title:
        return "海軍陸戰隊"
    if "海軍" in title or "海艦" in title:
        return "海軍艦艇兵"
    if "空軍" in title:
        return "空軍"
    return "陸軍"


def _normalize_batch(batch: str) -> str:
    try:
        return str(int(batch))
    except (TypeError, ValueError):
        return batch.strip()


def _camp_key(camp: str) -> str:
    known_camps = (
        "成功嶺",
        "斗煥坪",
        "犁頭山",
        "金六結",
        "北埔",
        "中坑",
        "龍泉",
        "左營",
    )
    return next((name for name in known_camps if name in camp), _clean_text(camp))


def _schedule_base_key(schedule: dict[str, Any]) -> tuple[str, str, str]:
    return (
        schedule["branch"],
        _normalize_batch(schedule["batch"]),
        schedule["enlistment_date"],
    )


def _schedule_match_key(schedule: dict[str, Any]) -> tuple[str, str, str, str]:
    return (*_schedule_base_key(schedule), _camp_key(schedule.get("camp", "")))


def _compact_pdf_text(value: str) -> str:
    value = value.replace("\u3000", " ").replace("\xa0", " ")
    value = re.sub(r"(?<=\d)\s+(?=\d)", "", value)
    return re.sub(r"\s+", "", value)


def _extract_pdf_training_camp(compact_text: str) -> str | None:
    """以 PDF「收訓單位」後方括號內的營區為準。"""
    training_unit_section = compact_text.split("收訓單位", maxsplit=1)
    if len(training_unit_section) != 2:
        return None

    section = re.split(
        r"入營日期|入營日|受訓時間|郵政信箱|聯絡電話|宣導事項",
        training_unit_section[1],
        maxsplit=1,
    )[0]
    matches = re.findall(r"[（(]([^）()]*營區)[）)]", section)
    return _clean_text(matches[-1]) if matches else None


def _extract_labeled_values(
    text: str,
    labels: tuple[str, ...],
    stop_markers: tuple[str, ...] = (),
    followed_by_date: bool = False,
) -> list[tuple[str, str]]:
    ordered_labels = sorted(labels, key=len, reverse=True)
    marker_pattern = "|".join(re.escape(label) for label in ordered_labels)
    if followed_by_date:
        marker_pattern = f"(?:{marker_pattern})(?=\\d{{1,3}}年|\\d{{1,2}}月)"
    matches = list(re.finditer(marker_pattern, text))
    values: list[tuple[str, str]] = []

    for index, match in enumerate(matches):
        value_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        value = text[match.end() : value_end]
        for marker in stop_markers:
            value = value.split(marker, maxsplit=1)[0]
        value = value.strip("：:;；,，。 ")
        if value:
            values.append((match.group(), value))
    return values


def _event_type(label: str) -> str:
    type_keywords = (
        ("family", ("懇親",)),
        ("leave", ("休假", "例假", "結訓假")),
        ("lottery", ("抽籤", "憲抽")),
        ("assessment", ("鑑測", "艦測", "測驗")),
        ("assignment", ("撥交",)),
        ("completion", ("結訓", "退伍")),
        ("selection", ("選填", "選兵", "憲選")),
        ("training", ("訓練", "專長", "游泳")),
    )
    for event_type, keywords in type_keywords:
        if any(keyword in label for keyword in keywords):
            return event_type
    return "other"


def _parse_schedule(item: Any) -> dict[str, Any] | None:
    paragraphs = [
        _clean_text(paragraph.get_text(" ", strip=True))
        for paragraph in item.find_all("p")
        if _clean_text(paragraph.get_text(" ", strip=True))
    ]
    if len(paragraphs) < 2:
        return None

    enlistment = _parse_roc_date(paragraphs[0])
    if not enlistment:
        return None

    raw_title = paragraphs[1]
    title = strip_camp_from_title(raw_title)
    schedule_id = hashlib.sha1(
        f"{enlistment.isoformat()}|{raw_title}".encode("utf-8")
    ).hexdigest()[:12]
    branch = _normalize_branch(raw_title)

    batch_match = re.search(r"第\s*([0-9]+)\s*梯", raw_title)
    batch = batch_match.group(1) if batch_match else "未標示"
    camp_match = re.search(r"[（(]([^）)]*營區)[）)]", raw_title)
    camp = camp_match.group(1) if camp_match else "未標示營區"

    details = []
    events = [
        {
            "id": f"{schedule_id}-enlistment",
            "title": "入營",
            "type": "enlistment",
            "start_date": enlistment.isoformat(),
            "end_date": enlistment.isoformat(),
            "description": paragraphs[0],
        }
    ]

    for detail_index, line in enumerate(paragraphs[2:]):
        if "本資料為預劃行程僅供參考" in line:
            continue

        parts = re.split(r"[：:]", line, maxsplit=1)
        if len(parts) == 2:
            label, value = (_clean_text(part) for part in parts)
        else:
            label, value = "其他資訊", line

        details.append({"label": label, "value": value})
        for date_index, (start, end) in enumerate(
            _extract_event_dates(value, enlistment)
        ):
            events.append(
                {
                    "id": f"{schedule_id}-{detail_index}-{date_index}",
                    "title": label,
                    "type": _event_type(label),
                    "start_date": start.isoformat(),
                    "end_date": end.isoformat(),
                    "description": value,
                }
            )

    return {
        "id": schedule_id,
        "branch": branch,
        "batch": batch,
        "title": title,
        "camp": camp,
        "enlistment_date": enlistment.isoformat(),
        "enlistment_date_roc": paragraphs[0].removesuffix("入營"),
        "details": details,
        "events": events,
        "sources": [PRIMARY_SOURCE.copy()],
    }


def _parse_taipei_listing_entry(row: Any) -> dict[str, Any] | None:
    link = row.select_one("td[data-title='主題'] a")
    if not link:
        return None

    listing_title = _clean_text(link.get_text(" ", strip=True))
    if "入營" not in listing_title or "替代役" in listing_title:
        return None

    enlistment = _parse_roc_date(listing_title)
    batch_match = re.search(r"(?:第\s*)?0*([0-9]+)\s*梯", listing_title)
    if not enlistment or not batch_match:
        return None

    raw_title = listing_title.split("入營", maxsplit=1)[1]
    camp_match = re.search(r"[（(]([^）)]*營區)\s*[）)]", raw_title)
    published_cell = row.select_one("td[data-title='上版日期']")
    return {
        "listing_title": listing_title,
        "title": strip_camp_from_title(raw_title),
        "branch": _normalize_branch(raw_title),
        "batch": _normalize_batch(batch_match.group(1)),
        "camp": _clean_text(camp_match.group(1)) if camp_match else "未標示營區",
        "enlistment_date": enlistment.isoformat(),
        "enlistment_date_roc": (
            f"{enlistment.year - 1911}年{enlistment.month}月{enlistment.day}日"
        ),
        "pdf_url": urljoin(TAIPEI_SOURCE_URL, link.get("href", "")),
        "published_at": (
            _clean_text(published_cell.get_text(" ", strip=True))
            if published_cell
            else None
        ),
    }


def _fetch_taipei_listing(session: requests.Session) -> list[dict[str, Any]]:
    response = session.get(
        f"{TAIPEI_SOURCE_URL}&page=1&PageSize=100",
        headers=REQUEST_HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.content.decode("utf-8-sig", errors="replace"), "lxml")
    entries = []
    for row in soup.select("td[data-title='主題']"):
        entry = _parse_taipei_listing_entry(row.parent)
        if entry:
            entries.append(entry)
    return entries


def _parse_taipei_pdf_text(
    entry: dict[str, Any],
    extracted_text: str,
) -> dict[str, Any] | None:
    enlistment = date.fromisoformat(entry["enlistment_date"])
    compact_text = _compact_pdf_text(extracted_text)
    if not compact_text:
        return None
    pdf_camp = _extract_pdf_training_camp(compact_text) or entry["camp"]

    schedule_id = hashlib.sha1(
        f"taipei|{entry['enlistment_date']}|{entry['listing_title']}".encode("utf-8")
    ).hexdigest()[:12]
    details: list[dict[str, Any]] = []
    events = [
        {
            "id": f"{schedule_id}-enlistment",
            "title": "入營",
            "type": "enlistment",
            "start_date": entry["enlistment_date"],
            "end_date": entry["enlistment_date"],
            "description": entry["enlistment_date_roc"],
            "source": "taipei",
        }
    ]

    calendar_text = compact_text.split("重要行事曆", maxsplit=1)[-1]
    calendar_fields = _extract_labeled_values(
        calendar_text,
        _taipei_calendar_labels,
        stop_markers=("※", "上列時間僅供參考"),
        followed_by_date=True,
    )
    for detail_index, (label, value) in enumerate(calendar_fields):
        details.append({"label": label, "value": value, "source": "taipei"})
        for date_index, (start, end) in enumerate(
            _extract_event_dates(value, enlistment)
        ):
            events.append(
                {
                    "id": f"{schedule_id}-{detail_index}-{date_index}",
                    "title": label,
                    "type": _event_type(label),
                    "start_date": start.isoformat(),
                    "end_date": end.isoformat(),
                    "description": value,
                    "source": "taipei",
                }
            )

    if len(events) == 1 and not details:
        return None

    source = {
        **TAIPEI_SOURCE,
        "url": entry["pdf_url"],
        "published_at": entry.get("published_at"),
    }
    return {
        "id": schedule_id,
        "branch": entry["branch"],
        "batch": entry["batch"],
        "title": entry["title"],
        "camp": pdf_camp,
        "enlistment_date": entry["enlistment_date"],
        "enlistment_date_roc": entry["enlistment_date_roc"],
        "details": details,
        "events": events,
        "sources": [source],
        "supplementary_only": True,
    }


def _fetch_taipei_pdf_schedule(
    session: requests.Session,
    entry: dict[str, Any],
) -> dict[str, Any] | None:
    response = session.get(entry["pdf_url"], headers=REQUEST_HEADERS, timeout=30)
    response.raise_for_status()
    reader = PdfReader(BytesIO(response.content))
    extracted_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return _parse_taipei_pdf_text(entry, extracted_text)


def _add_taipei_new_schedules(
    primary_schedules: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    session = requests.Session()
    entries = _fetch_taipei_listing(session)
    if not entries:
        raise ValueError("臺北市來源頁面中找不到可解析的國軍梯次 PDF")

    latest_primary_date = max(
        date.fromisoformat(schedule["enlistment_date"])
        for schedule in primary_schedules
    )
    primary_base_keys = {_schedule_base_key(schedule) for schedule in primary_schedules}
    candidate_entries = []
    for entry in entries:
        entry_base_key = (
            entry["branch"],
            _normalize_batch(entry["batch"]),
            entry["enlistment_date"],
        )
        entry_date = date.fromisoformat(entry["enlistment_date"])
        if entry_base_key in primary_base_keys or entry_date >= latest_primary_date - timedelta(days=7):
            candidate_entries.append(entry)
        if len(candidate_entries) >= TAIPEI_MAX_PDFS:
            break

    supplementary_schedules = []
    pdf_errors = []
    for entry in candidate_entries:
        try:
            schedule = _fetch_taipei_pdf_schedule(session, entry)
            if schedule:
                supplementary_schedules.append(schedule)
        except Exception as error:
            pdf_errors.append(f"{entry['listing_title']}: {error}")

    merged_schedules = list(primary_schedules)
    skipped_existing_count = 0
    added_count = 0
    for supplementary in supplementary_schedules:
        exact_key = _schedule_match_key(supplementary)
        base_key = _schedule_base_key(supplementary)
        match_index = next(
            (
                index
                for index, schedule in enumerate(merged_schedules)
                if _schedule_match_key(schedule) == exact_key
            ),
            None,
        )
        if match_index is None:
            base_matches = [
                index
                for index, schedule in enumerate(merged_schedules)
                if _schedule_base_key(schedule) == base_key
            ]
            if len(base_matches) == 1:
                primary_camp = merged_schedules[base_matches[0]].get("camp", "")
                supplementary_camp = supplementary.get("camp", "")
                if "未標示" in primary_camp or "未標示" in supplementary_camp:
                    match_index = base_matches[0]

        if match_index is None:
            merged_schedules.append(supplementary)
            added_count += 1
            _print_calendar_progress(
                "採用 PDF 新梯次："
                f"{supplementary['branch']} 第{supplementary['batch']}梯｜"
                f"{supplementary['camp']}"
            )
        else:
            skipped_existing_count += 1

    source_status = {
        **TAIPEI_SOURCE,
        "status": "ok" if supplementary_schedules else "no_data",
        "listed_count": len(entries),
        "processed_pdf_count": len(candidate_entries),
        "parsed_pdf_count": len(supplementary_schedules),
        "skipped_existing_count": skipped_existing_count,
        "added_count": added_count,
    }
    if pdf_errors:
        source_status["errors"] = pdf_errors[:5]
        source_status["failed_pdf_count"] = len(pdf_errors)
    return merged_schedules, source_status


def scrape_troop_calendar() -> dict[str, Any]:
    response = requests.get(
        SOURCE_URL,
        headers=REQUEST_HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.content.decode("utf-8", errors="replace"), "lxml")
    items = soup.select("#searchResults li.list-divider")
    if not items:
        raise ValueError("來源頁面中找不到部隊行事曆資料")

    schedules = []
    for item in items:
        schedule = _parse_schedule(item)
        if schedule:
            schedules.append(schedule)

    if not schedules:
        raise ValueError("來源頁面資料格式無法解析")

    primary_count = len(schedules)
    primary_status = {
        **PRIMARY_SOURCE,
        "status": "ok",
        "schedule_count": primary_count,
    }
    try:
        schedules, taipei_status = _add_taipei_new_schedules(schedules)
    except Exception as error:
        taipei_status = {
            **TAIPEI_SOURCE,
            "status": "error",
            "error": str(error),
        }

    schedules.sort(
        key=lambda schedule: (schedule["enlistment_date"], schedule["title"]),
        reverse=True,
    )
    fetched_at = datetime.now(timezone.utc).isoformat()
    return {
        "schema_version": CACHE_SCHEMA_VERSION,
        "source": SOURCE_URL,
        "sources": [primary_status, taipei_status],
        "fetched_at": fetched_at,
        "branches": ["陸軍", "海軍艦艇兵", "海軍陸戰隊", "空軍"],
        "count": len(schedules),
        "schedules": schedules,
    }


def _read_cache() -> dict[str, Any] | None:
    try:
        with CACHE_PATH.open("r", encoding="utf-8") as cache_file:
            return json.load(cache_file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _write_cache(payload: dict[str, Any]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = CACHE_PATH.with_suffix(".tmp")
    with temporary_path.open("w", encoding="utf-8") as cache_file:
        json.dump(payload, cache_file, ensure_ascii=False, indent=2)
    temporary_path.replace(CACHE_PATH)


def _is_compatible(payload: dict[str, Any]) -> bool:
    return payload.get("schema_version") == CACHE_SCHEMA_VERSION


def _is_fresh(payload: dict[str, Any]) -> bool:
    try:
        if not _is_compatible(payload):
            return False
        fetched_at = datetime.fromisoformat(payload["fetched_at"])
        return datetime.now(timezone.utc) - fetched_at < CACHE_TTL
    except (KeyError, TypeError, ValueError):
        return False


def get_troop_calendar() -> dict[str, Any]:
    with _cache_lock:
        cached = _read_cache()
        if cached and _is_fresh(cached):
            return {
                **cached,
                "cache": {"status": "hit", "max_age_seconds": 86400},
            }

        try:
            payload = scrape_troop_calendar()
            _write_cache(payload)
            return {
                **payload,
                "cache": {"status": "refreshed", "max_age_seconds": 86400},
            }
        except Exception as error:
            if cached and _is_compatible(cached):
                return {
                    **cached,
                    "cache": {
                        "status": "stale",
                        "max_age_seconds": 86400,
                        "error": str(error),
                    },
                }
            raise
