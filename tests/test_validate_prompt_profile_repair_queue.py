from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.validate_prompt_profile_repair_queue import assert_same


class ValidatePromptProfileRepairQueueTests(unittest.TestCase):
    def test_assert_same_reports_stale_actual_file(self) -> None:
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

    def test_assert_same_accepts_matching_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            expected = root / "expected.json"
            actual = root / "actual.json"
            expected.write_text('{"rows": []}\n', encoding="utf-8")
            actual.write_text('{"rows": []}\n', encoding="utf-8")
            failures: list[str] = []

            assert_same(expected, actual, failures)

        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
