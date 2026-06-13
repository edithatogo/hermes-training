from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_standard_benchmark_coverage_reports import assert_same


class ValidateStandardBenchmarkCoverageReportsTests(unittest.TestCase):
    def test_assert_same_reports_stale_standard_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected = tmpdir / "expected.json"
            actual = tmpdir / "actual.json"
            expected.write_text('{"status": "pilot-only"}\n', encoding="utf-8")
            actual.write_text('{"status": "incomplete"}\n', encoding="utf-8")

            failures: list[str] = []
            assert_same(expected, actual, failures)

        self.assertTrue(any("is stale" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
