import unittest

from bs4 import BeautifulSoup

from services.troop_calendar import (
    _parse_taipei_listing_entry,
    _parse_taipei_pdf_text,
)


class TaipeiCalendarParserTest(unittest.TestCase):
    def setUp(self):
        self.entry = {
            "listing_title": (
                "115年9月22日入營海軍陸戰常備兵役軍事訓練"
                "第126梯次(海軍陸戰隊新兵訓練中心屏東龍泉營區)"
            ),
            "title": "海軍陸戰常備兵役軍事訓練第126梯次",
            "branch": "海軍陸戰隊",
            "batch": "126",
            "camp": "海軍陸戰隊新兵訓練中心屏東龍泉營區",
            "enlistment_date": "2026-09-22",
            "enlistment_date_roc": "115年9月22日",
            "pdf_url": "https://example.test/126.pdf",
            "published_at": "115-09-16",
        }

    def test_listing_accepts_batch_without_prefix_character(self):
        soup = BeautifulSoup(
            """
            <tr>
              <td data-title="主題"><a href="/2256.pdf">
                115年9月16日入營陸軍常備兵2256梯次(新竹犁頭山營區)
              </a></td>
              <td data-title="上版日期">115-09-11</td>
            </tr>
            """,
            "lxml",
        )
        entry = _parse_taipei_listing_entry(soup.select_one("tr"))
        self.assertIsNotNone(entry)
        self.assertEqual(entry["batch"], "2256")
        self.assertEqual(entry["camp"], "新竹犁頭山營區")

    def test_pdf_parser_repairs_split_roc_year_and_multiple_ranges(self):
        schedule = _parse_taipei_pdf_text(
            self.entry,
            """
            收 訓 單 位 海軍陸戰隊新兵訓練中心（屏東龍泉營區）
            入 營 日 期 11\n5年9月22日
            受訓時間 115年9月22日~12月1日
            郵政信箱 屏東龍泉郵政90219附10號信箱
            聯絡電話 08-7700052
            宣導事項
            重要行事曆 懇 親 115年10月3日
            休假 10月3~9日、10月22~28日
            結訓 116年1月12日零時生效（無折抵役期之退伍日）
            ※上列時間僅供參考
            """,
        )
        self.assertIsNotNone(schedule)
        self.assertEqual(schedule["camp"], "屏東龍泉營區")
        self.assertFalse(
            {"受訓時間", "郵政信箱", "聯絡電話"}
            & {detail["label"] for detail in schedule["details"]}
        )
        event_ranges = {
            (event["type"], event["start_date"], event["end_date"])
            for event in schedule["events"]
        }
        self.assertIn(("family", "2026-10-03", "2026-10-03"), event_ranges)
        self.assertIn(("leave", "2026-10-03", "2026-10-09"), event_ranges)
        self.assertIn(("leave", "2026-10-22", "2026-10-28"), event_ranges)
        self.assertIn(("completion", "2027-01-12", "2027-01-12"), event_ranges)

if __name__ == "__main__":
    unittest.main()
