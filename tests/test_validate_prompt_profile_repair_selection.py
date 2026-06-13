from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.validate_prompt_profile_repair_selection import assert_same


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


if __name__ == "__main__":
    unittest.main()
