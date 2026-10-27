import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import search  # noqa: E402

UNITS = [{
    "id": "u1", "title": "Unit One",
    "concepts": [
        {"id": "u1-state", "title": "State File", "text_md": "The terraform.tfstate file is Terraform's memory."},
        {"id": "u1-mod", "title": "Modules", "text_md": "Reusable code, write once. Mentions state only briefly."},
    ],
    "questions": [
        {"id": "u1-q01", "title": "What is Docker?", "prompt": "What is Docker?", "reference_answer": "A container platform."},
    ],
}]


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.idx = search.SearchIndex(UNITS)

    def test_fts_available_here(self):
        self.assertTrue(self.idx.use_fts)

    def test_title_match_ranks_above_body_match(self):
        hits = self.idx.search("state")
        self.assertEqual(hits[0]["item_id"], "u1-state")
        self.assertIn("u1-mod", [h["item_id"] for h in hits])

    def test_prefix_and_questions(self):
        self.assertEqual(self.idx.search("contain")[0]["item_id"], "u1-q01")
        self.assertEqual(self.idx.search("contain")[0]["kind"], "question")

    def test_snippet_markers(self):
        self.assertIn("[[", self.idx.search("memory")[0]["snippet"])

    def test_hostile_input_is_not_fts_syntax(self):
        for bad in ['"', "state AND", "NEAR(", "*", "a OR b -c", "col:state", "'; DROP TABLE docs;--", ""]:
            self.assertIsInstance(self.idx.search(bad), list)
        self.assertEqual(self.idx.search("   "), [])

    def test_all_terms_required(self):
        self.assertEqual(self.idx.search("docker terraform"), [])

    def test_limit_clamped(self):
        self.assertLessEqual(len(self.idx.search("state", limit=0)), 1)
        self.assertLessEqual(len(self.idx.search("state", limit=999)), 50)

    def test_fallback_without_fts(self):
        idx = search.SearchIndex(UNITS, use_fts=False)
        self.assertFalse(idx.use_fts)
        self.assertEqual(idx.search("memory")[0]["item_id"], "u1-state")

    def test_plain_strips_markdown_and_box_drawing(self):
        t = search.plain("**Bold** `code`\n```text\n \u251c\u2500\u2500 Provider\n```\n- item")
        self.assertNotIn("*", t)
        self.assertNotIn("`", t)
        self.assertNotIn("\u251c", t)
        self.assertIn("Provider", t)

    def test_snippets_are_plain_text(self):
        hit = self.idx.search("memory")[0]
        self.assertNotIn("**", hit["snippet"])

    def test_question_prompt_not_duplicated_in_title(self):
        hit = self.idx.search("docker")[0]
        self.assertEqual(hit["title"], "What is Docker?")

    def test_real_corpus(self):
        here = os.path.join(os.path.dirname(__file__), "..", "content")
        units = []
        for d in sorted(os.listdir(here)):
            p = os.path.join(here, d, "unit.json")
            if os.path.isfile(p):
                with open(p, encoding="utf-8") as f:
                    units.append(json.load(f))
        idx = search.SearchIndex(units)
        hits = idx.search("terraform state locking")
        self.assertTrue(hits)
        self.assertTrue(any(h["unit_id"] == "fw1" for h in hits))


if __name__ == "__main__":
    unittest.main()
