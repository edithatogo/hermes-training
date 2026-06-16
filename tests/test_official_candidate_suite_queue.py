import tempfile
import unittest
from pathlib import Path

from scripts.build_official_candidate_suite_queue import build_report, render_markdown
from scripts.validate_official_candidate_suite_queue import REQUIRED_SUITES, validate


class OfficialCandidateSuiteQueueTests(unittest.TestCase):
    def write_coverage(self, root: Path) -> Path:
        path = root / "coverage.json"
        path.write_text(
            """{
  "summary": {
    "official_candidate_missing": [
      "official-bfcl",
      "official-coding",
      "safety-refusal",
      "ruler-long-context"
    ]
  }
}
""",
            encoding="utf-8",
        )
        return path

    def test_queue_covers_all_missing_official_candidate_suites(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            coverage = self.write_coverage(Path(tmp))
            report = build_report(coverage)
        self.assertEqual(report["status"], "blocked-missing-official-candidates")
        self.assertEqual(tuple(report["missing_suites"]), REQUIRED_SUITES)
        by_suite = {item["suite"]: item for item in report["items"]}
        self.assertIn("bfcl generate", by_suite["official-bfcl"]["local_command"])
        self.assertIn("evalplus.evaluate", by_suite["official-coding"]["local_command"])
        self.assertIn("safety-refusal-suite", by_suite["safety-refusal"]["local_command"])
        self.assertIn("ruler.run", by_suite["ruler-long-context"]["local_command"])

    def test_generated_report_validates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            coverage = self.write_coverage(root)
            report = build_report(coverage)
            report_path = root / "queue.json"
            report_path.write_text(__import__("json").dumps(report), encoding="utf-8")
            self.assertEqual(validate(report_path), [])

    def test_markdown_keeps_publication_boundary_visible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            coverage = self.write_coverage(Path(tmp))
            markdown = render_markdown(build_report(coverage))
        self.assertIn("No public broad benchmark claim", markdown)
        self.assertIn("official-bfcl", markdown)


if __name__ == "__main__":
    unittest.main()
