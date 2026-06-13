from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_mem0_benchmark_index import assert_same, collect_summary_paths, extract_table


class ValidateMem0BenchmarkIndexTests(unittest.TestCase):
    def test_extract_table_preserves_only_generated_section(self) -> None:
        markdown = "# mem0 Benchmark Index\n\nCurated note.\n\n| Kind | Run ID |\n|---|---|\n| embedding | run-1 |\n"

        self.assertEqual(extract_table(markdown), "| Kind | Run ID |\n|---|---|\n| embedding | run-1 |\n")

    def test_assert_same_reports_stale_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected = tmpdir / "expected.md"
            actual = tmpdir / "actual.md"
            expected.write_text("# x\n\n| Kind | Run ID |\n|---|---|\n| embedding | old |\n", encoding="utf-8")
            actual.write_text("# x\n\n| Kind | Run ID |\n|---|---|\n| embedding | new |\n", encoding="utf-8")

            failures: list[str] = []
            assert_same(expected, actual, failures)

        self.assertTrue(any("is stale" in failure for failure in failures))

    def test_collect_summary_paths_uses_direct_benchmark_runs_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            direct = root / "embedding-benchmark" / "run-a" / "summary.json"
            nested = root / "mem0-memory-benchmark" / "run-b" / "rerank" / "nested" / "summary.json"
            direct.parent.mkdir(parents=True)
            nested.parent.mkdir(parents=True)
            direct.write_text("{}", encoding="utf-8")
            nested.write_text("{}", encoding="utf-8")

            paths = collect_summary_paths(root)

        self.assertEqual(paths, [direct])


if __name__ == "__main__":
    unittest.main()
