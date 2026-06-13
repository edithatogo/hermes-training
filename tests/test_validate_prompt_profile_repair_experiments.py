from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.validate_prompt_profile_repair_experiments import assert_same


class ValidatePromptProfileRepairExperimentsTests(unittest.TestCase):
    def test_assert_same_reports_stale_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            expected = root / "expected.json"
            actual = root / "actual.json"
            expected.write_text('{"fresh": true}\n', encoding="utf-8")
            actual.write_text('{"fresh": false}\n', encoding="utf-8")
            failures: list[str] = []

            assert_same(expected, actual, failures)

        self.assertEqual(len(failures), 1)
        self.assertIn("is stale; regenerate it", failures[0])


if __name__ == "__main__":
    unittest.main()
