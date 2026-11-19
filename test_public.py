"""公开版的轻量离线结构检查。"""
import re
import unittest
from pathlib import Path


HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")


class PublicBankTests(unittest.TestCase):
    def test_full_question_bank(self):
        match = re.search(
            r"(?ms)^const QUESTIONS = \[\s*\n(.*?)^\];\s*\nconst STORE_KEY=",
            HTML,
        )
        self.assertIsNotNone(match)
        ids = re.findall(
            r'(?m)^\s*\{\s*(?:id:\s*|"id"\s*:\s*)"([^"]+)"',
            match.group(1),
        )
        self.assertEqual(len(ids), 44)
        self.assertEqual(len(ids), len(set(ids)), "题目 ID 不可重复")
        self.assertIn("ch1_conversion_order", ids)
        self.assertIn("pwm4", ids)

    def test_existing_visitor_data_is_preserved(self):
        self.assertIn('const STORE_KEY="mcu_exam_station_public_demo_v1"', HTML)
        self.assertIn("localStorage", HTML)
        self.assertNotIn('const STORE_KEY="mcu_exam_station_v2"', HTML)

    def test_core_interactions_and_templates_exist(self):
        for element_id in (
            "questionDetail", "wrongList", "categoryProgress",
            "addQuestionBtn", "startStepBtn", "homeworkFilters",
            "view-reference", "view-templates",
        ):
            self.assertIn(f'id="{element_id}"', HTML)
        for homework in ("作业1", "作业2", "作业3", "作业4", "作业5"):
            self.assertIn(homework, HTML)

    def test_past_exam_ocr_text_order(self):
        self.assertIn('data-view="past-exam"', HTML)
        self.assertIn('id="view-past-exam"', HTML)
        self.assertIn("第 8 页未收到", HTML)
        marker_positions = [
            HTML.index(f'id="exam-question-{i}"') for i in range(1, 6)
        ]
        self.assertEqual(marker_positions, sorted(marker_positions))
        for i in range(1, 6):
            self.assertIn(f'href="#exam-question-{i}"', HTML)
        for key in ("9600 bit/s", "TH1=FAH", "0x9C", "0x7FF8",
                    "F = F * 1000.0 / 255", "Number %= 100"):
            self.assertIn(key, HTML)
        self.assertNotIn('src="assets/exams/', HTML)
        self.assertNotIn("<img", HTML)
        self.assertFalse((Path(__file__).parent / "assets" / "exams").exists())

    def test_no_local_paths_or_account_info(self):
        self.assertNotRegex(HTML, r"[A-Za-z]:\\")
        self.assertNotRegex(
            HTML, r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        )


if __name__ == "__main__":
    unittest.main()
