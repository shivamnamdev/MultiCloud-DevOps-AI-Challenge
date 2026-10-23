import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import ingest  # noqa: E402


class IngestFw1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = ingest.build_unit(ingest.UNITS[0])
        cls.concepts = {c["id"]: c for c in cls.unit["concepts"]}

    def test_counts(self):
        qs = self.unit["questions"]
        self.assertEqual(sum(q["kind"] == "interview" for q in qs), 25)
        self.assertEqual(sum(q["kind"] == "scenario" for q in qs), 25)
        self.assertGreaterEqual(len(self.concepts), 20)

    def test_noise_excluded(self):
        blob = " ".join(c["text_md"] for c in self.unit["concepts"])
        # note: "WhatsApp" and "₹2" legitimately remain inside the AWS-account practical
        for bad in ("Enrollment", "Early bird", "Mithun", "shields.io", "999-344"):
            self.assertNotIn(bad, blob)

    def test_word_boundary_linking(self):
        by_id = {q["id"]: q for q in self.unit["questions"]}
        self.assertNotIn("fw1-data-source", by_id["fw1-q04"]["concept_ids"])
        self.assertIn("fw1-resources", by_id["fw1-q04"]["concept_ids"])

    def test_artefacts_cleaned(self):
        self.assertNotIn("****", " ".join(c["text_md"] for c in self.unit["concepts"]))
        self.assertIn("fw1-state-file-terraform-tfstate", self.concepts)

    def test_expected_concepts_present(self):
        for slug in ("provider", "modules", "backend", "dependency-graph", "workspace",
                     "terraform-vs-ansible", "quick-revision-map", "essential-terraform-commands",
                     "ec2-instance-provisioning-via-terraform"):
            self.assertIn("fw1-" + slug, self.concepts)

    def test_questions_have_answers_and_links(self):
        for q in self.unit["questions"]:
            self.assertTrue(q["reference_answer"], q["id"])
            for cid in q["concept_ids"]:
                self.assertIn(cid, self.concepts)
        by_id = {q["id"]: q for q in self.unit["questions"]}
        self.assertIn("fw1-provider", by_id["fw1-q03"]["concept_ids"])
        self.assertIn("fw1-modules", by_id["fw1-s13"]["concept_ids"] + by_id["fw1-q15"]["concept_ids"])

    def test_scenario_split(self):
        s = {q["id"]: q for q in self.unit["questions"]}["fw1-s01"]
        self.assertTrue(s["prompt"].startswith("Two engineers"))
        self.assertIn("state locking", s["reference_answer"])

    def test_heading_in_fence_ignored(self):
        lines = ["## A", "```", "## not a heading", "```", "## B"]
        self.assertEqual([t for t, _ in ingest.sections(lines, 2)], ["A", "B"])


if __name__ == "__main__":
    unittest.main()
