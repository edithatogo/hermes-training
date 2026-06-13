from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_mem0_candidate_queue import assert_same


class ValidateMem0CandidateQueueTests(unittest.TestCase):
    def test_assert_same_reports_stale_queue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected = tmpdir / "expected.md"
            actual = tmpdir / "actual.md"
            expected.write_text("# Queue\n\nnew\n", encoding="utf-8")
            actual.write_text("# Queue\n\nold\n", encoding="utf-8")

            failures: list[str] = []
            assert_same(expected, actual, failures)

        self.assertTrue(any("is stale" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
