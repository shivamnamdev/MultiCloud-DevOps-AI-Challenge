import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import ingest  # noqa: E402


def parse(md):
    return ingest.parse_generic(md, "t")


class GenericParserTest(unittest.TestCase):
    def test_h2_sections_with_h3_children_become_concepts(self):
        r = parse("# Title\n## Core Concepts\n### Alpha\n" + "alpha detail text " * 5 + "\n### Beta\n" + "beta detail text " * 5 + "\n")
        self.assertEqual([c["title"] for c in r["concepts"]], ["Alpha", "Beta"])

    def test_h3_directly_under_title(self):
        r = parse("# Title\n### 1. Session Overview\n" + "overview text " * 8 + "\n### 2. Node Pools\n" + "pool text " * 8 + "\n")
        self.assertEqual([c["title"] for c in r["concepts"]], ["Session Overview", "Node Pools"])

    def test_noise_h2_does_not_swallow_h3_content(self):
        r = parse("# T\n## Key Outcomes\nsummary\n### Real Topic\n" + "real topic body " * 8 + "\n### Action Items\n" + "do this later " * 8 + "\n")
        self.assertEqual([c["title"] for c in r["concepts"]], ["Real Topic"])

    def test_question_formats_and_emoji_answer_marker(self):
        md = ("# T\n## Interview Questions\n### ❓ Q1: What is Docker?\n\n**\U0001F4A1 Answer:**\n\nA container tool.\n"
              "### \U0001F4CC 10. Scenario: Pod is not running?\n\n**Answer:** Check events.\n"
              "### 3. Why use it?\n**Answer:** Portability.\n")
        r = parse(md)
        kinds = [(q["kind"], q["title"], q["reference_answer"]) for q in r["questions"]]
        self.assertEqual(kinds[0], ("interview", "What is Docker?", "A container tool."))
        self.assertEqual(kinds[1][0], "scenario")
        self.assertEqual(kinds[2], ("interview", "Why use it?", "Portability."))
        self.assertEqual([q["id"] for q in r["questions"]], ["t-q01", "t-s01", "t-q02"])

    def test_scenario_question_answer_markers(self):
        md = "# T\n## 20 Scenario Questions\n### Scenario 1: Locking\n**Question:** Two run apply?\n**Answer:** Use locking.\n"
        q = parse(md)["questions"][0]
        self.assertEqual((q["prompt"], q["reference_answer"]), ("Two run apply?", "Use locking."))

    def test_bare_scenario_without_answer_is_recorded_not_invented(self):
        md = "# T\n## Scenario Interview Questions\n### \U0001F4CC Scenario 1\n\nPR has a merge conflict.\n> **Question: how to resolve?**\n"
        r = parse(md)
        self.assertEqual(r["questions"], [])
        self.assertEqual(r["unanswered"], ["Scenario 1"])

    def test_non_qa_section_mentioning_scenario_stays_a_concept(self):
        r = parse("# T\n## Banking Scenario - Lifecycle Policy\n" + "policy text " * 20 + "\n")
        self.assertEqual(len(r["concepts"]), 1)
        self.assertEqual(r["unparsed"], [])

    def test_flat_long_bullet_section_is_flagged(self):
        body = "\n".join("- point number %d with some words in it to add length here" % i for i in range(60))
        r = parse("# T\n## Core Concepts Covered\n" + body + "\n")
        self.assertEqual(len(r["concepts"]), 1)
        self.assertEqual(r["flat"][0]["section"], "Core Concepts Covered")

    def test_artifacts_cleaned(self):
        r = parse("# T\n## Topic\n" + "text fileciteturn0file0L20-L45 more words here " * 3 + "\n")
        self.assertNotIn("filecite", r["concepts"][0]["text_md"])
        self.assertNotIn("", r["concepts"][0]["text_md"])

    def test_light_unit(self):
        md = ("# S\n## \U0001F3AF Topics Covered in Session 14\n- ALB\n- NLB\n"
              "### \U0001F528 Task-027: Create ALB\n```\nstatus\n```\n## \U0001F4A1 Key Learnings from Session 14\n\n> **1.** ALB is layer 7\n> **2.** NLB is layer 4\n")
        r = ingest.parse_light(md, "s14")
        self.assertEqual([c["title"] for c in r["concepts"]], ["Topics covered", "Key learnings", "Task 027"])
        self.assertIn("- ALB is layer 7", r["concepts"][1]["text_md"])


class CorpusInvariantsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.units = ingest.build_all()

    def test_ids_unique_across_corpus(self):
        ids = [x["id"] for u in self.units for x in u["concepts"] + u["questions"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_session_with_content_is_covered(self):
        sessions = {u["session"] for u in self.units}
        for n in range(0, 60):
            self.assertIn(n, sessions, "session %d has no unit" % n)

    def test_every_question_has_answer_and_valid_links(self):
        for u in self.units:
            cids = {c["id"] for c in u["concepts"]}
            for q in u["questions"]:
                self.assertTrue(q["reference_answer"].strip(), q["id"])
                self.assertTrue(set(q["concept_ids"]) <= cids)

    def test_no_pua_or_filecite_artifacts(self):
        for u in self.units:
            for c in u["concepts"]:
                self.assertNotIn("filecite", c["text_md"])
                self.assertFalse(any("" <= ch <= "" for ch in c["text_md"]), c["id"])

    def test_light_units_only_for_sessions_without_notes(self):
        notes = {u["session"] for u in self.units if u["status"] != "light"}
        for u in self.units:
            if u["status"] == "light":
                self.assertNotIn(u["session"], notes)


if __name__ == "__main__":
    unittest.main()
