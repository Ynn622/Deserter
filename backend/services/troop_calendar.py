import hashlib
import json
import os
import re
import threading
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


SOURCE_URL = "https://soldier.ntpc.gov.tw/mt6480"
CACHE_TTL = timedelta(days=1)
CACHE_SCHEMA_VERSION = 2
CACHE_PATH = Path(
    os.getenv(
        "TROOP_CALENDAR_CACHE_PATH",
        Path(__file__).resolve().parents[1] / "cache" / "troop_calendar.json",
    )
)

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
    }


def scrape_troop_calendar() -> dict[str, Any]:
    response = requests.get(
        SOURCE_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; DeserterCalendar/1.0; "
                "+https://github.com/)"
            )
        },
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

    schedules.sort(
        key=lambda schedule: (schedule["enlistment_date"], schedule["title"]),
        reverse=True,
    )
    fetched_at = datetime.now(timezone.utc).isoformat()
    return {
        "schema_version": CACHE_SCHEMA_VERSION,
        "source": SOURCE_URL,
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
