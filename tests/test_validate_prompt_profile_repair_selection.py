from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.validate_prompt_profile_repair_selection import assert_same, expected_default


class ValidatePromptProfileRepairSelectionTests(unittest.TestCase):
    def test_assert_same_reports_stale_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            expected = root / "expected.md"
            actual = root / "actual.md"
            expected.write_text("fresh\n", encoding="utf-8")
            actual.write_text("stale\n", encoding="utf-8")
            failures: list[str] = []

            assert_same(expected, actual, failures)

        self.assertEqual(len(failures), 1)
        self.assertIn("is stale; regenerate it", failures[0])

    def test_expected_default_allows_exhausted_queue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            experiments = root / "experiments.json"
            results = root / "results.json"
            experiments.write_text(
                '{"experiments":[{"candidate":"a","variant":"v1","runner":"local"}]}',
                encoding="utf-8",
            )
            results.write_text(
                '{"results":[{"candidate":"a","variant":"v1"}]}',
                encoding="utf-8",
            )

            expected = expected_default(experiments, results)

        self.assertEqual(expected["runner"], "none")
        self.assertIsNone(expected["candidate"])


if __name__ == "__main__":
    unittest.main()
