from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.check_standard_benchmark_coverage import build_items, main, render_markdown, summarize


class StandardBenchmarkCoverageTests(unittest.TestCase):
    def test_qwen3_v4_coverage_marks_pilot_only(self) -> None:
        items = build_items("qwen3-4b-strict-toolcall-v4-targeted")
        summary = summarize(items, "qwen3-4b-strict-toolcall-v4-targeted", "test-run")

        self.assertEqual(summary["status"], "pilot-only")
        self.assertTrue(summary["local_adapter_gate_ready"])
        self.assertTrue(summary["public_release_blocked"])
        self.assertIn("official-bfcl", summary["official_candidate_missing"])
        self.assertIn("lm-eval-selected", summary["official_candidate_missing"])
        statuses = {item["suite"]: item["status"] for item in summary["items"]}
        self.assertEqual(statuses["lm-eval-selected-smoke"], "present")
        self.assertEqual(statuses["lm-eval-selected"], "missing")
        metrics = {item["suite"]: item["metric"] for item in summary["items"]}
        self.assertEqual(metrics["local-bfcl-style-pilot"], "BFCL-style pilot 0.667")
        self.assertEqual(metrics["official-ifeval-pilot"], "prompt strict 0.760")
        self.assertEqual(metrics["lm-eval-selected-smoke"], "limit 10 selected MLX direct smoke scored")

    def test_markdown_lists_missing_official_suites(self) -> None:
        summary = summarize(build_items("qwen3-4b-strict-toolcall-v4-targeted"), "qwen3-4b-strict-toolcall-v4-targeted", "test-run")
        markdown = render_markdown(summary)

        self.assertIn("official-bfcl", markdown)
        self.assertIn("lm-eval-selected-smoke", markdown)
        self.assertIn("pilot-only", markdown)
        self.assertIn("local-heldout-strict-tool-call", markdown)

    def test_no_write_cli_prints_summary_without_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp)
            stdout = io.StringIO()
            argv = [
                "check_standard_benchmark_coverage.py",
                "--run-id",
                "test-run",
                "--output-root",
                str(output_root),
                "--no-write",
            ]
            with patch("sys.argv", argv), contextlib.redirect_stdout(stdout):
                code = main()

            self.assertEqual(code, 0)
            self.assertFalse((output_root / "test-run.json").exists())
            data = json.loads(stdout.getvalue())
            self.assertEqual(data["run_id"], "test-run")


if __name__ == "__main__":
    unittest.main()
