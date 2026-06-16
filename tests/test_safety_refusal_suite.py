import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts.materialize_safety_refusal_suite import build_suite, render_markdown
from scripts.run_tool_call_benchmark import validate_suite
from scripts.validate_safety_refusal_suite import validate_manifest


class SafetyRefusalSuiteTests(unittest.TestCase):
    def test_materialized_suite_is_valid_and_refusal_focused(self) -> None:
        suite = build_suite()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "suite.json"
            validate_suite(suite, path)
        invalid = [case for case in suite if case["category"] == "invalid_tool_handling"]
        self.assertGreaterEqual(len(invalid), 5)
        for case in invalid:
            self.assertEqual(case["expected"]["mode"], "text")
            self.assertTrue(case["expected"]["must_not_have_tool_calls"])
            self.assertTrue(case["expected"]["must_not_contain_any"])

    def test_validator_accepts_materialized_suite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "suite.json"
            path.write_text(__import__("json").dumps(build_suite()), encoding="utf-8")
            self.assertEqual(validate_manifest(path), [])

    def test_markdown_preserves_score_boundary(self) -> None:
        markdown = render_markdown(build_suite(), "2026-06-16T00:00:00+00:00")
        self.assertIn("not scored benchmark evidence", markdown)
        self.assertIn("safety-refusal-delete-customer-record", markdown)


if __name__ == "__main__":
    unittest.main()
