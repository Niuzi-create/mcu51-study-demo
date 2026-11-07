"""公开演示版的轻量离线结构检查。"""
import json
import re
import unittest
from pathlib import Path


HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")


class PublicDemoTests(unittest.TestCase):
    def test_only_original_demo_questions(self):
        match = re.search(r"const QUESTIONS = (\[[\s\S]*?\]);\s*const STORE_KEY=", HTML)
        self.assertIsNotNone(match)
        questions = json.loads(match.group(1))
        self.assertEqual(len(questions), 6)
        self.assertTrue(all(q["source"] == "原创演示题" for q in questions))

    def test_isolated_browser_storage(self):
        self.assertIn('const STORE_KEY="mcu_exam_station_public_demo_v1"', HTML)
        self.assertNotIn('const STORE_KEY="' + "mcu_exam_station_" + 'v2"', HTML)

    def test_core_interaction_elements_exist(self):
        for element_id in ("questionDetail", "wrongList", "categoryProgress",
                           "addQuestionBtn", "startStepBtn"):
            if element_id == "startStepBtn":
                self.assertIn('id="startStepBtn"', HTML)
            else:
                self.assertIn(f'id="{element_id}"', HTML)

    def test_no_private_course_content(self):
        for phrase in ("老师作业", "答题模板", "document\\新上传", "\u5929\u6d25"):
            self.assertNotIn(phrase, HTML)


if __name__ == "__main__":
    unittest.main()
