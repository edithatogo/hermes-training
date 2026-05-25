from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_standard_benchmark_coverage import build_items, render_markdown, summarize


class StandardBenchmarkCoverageTests(unittest.TestCase):
    def test_qwen3_v4_coverage_marks_pilot_only(self) -> None:
        items = build_items("qwen3-4b-strict-toolcall-v4-targeted")
        summary = summarize(items, "qwen3-4b-strict-toolcall-v4-targeted", "test-run")

        self.assertEqual(summary["status"], "pilot-only")
        self.assertTrue(summary["local_adapter_gate_ready"])
        self.assertTrue(summary["public_release_blocked"])
        self.assertIn("official-bfcl", summary["official_candidate_missing"])
        self.assertNotIn("lm-eval-selected", summary["official_candidate_missing"])
        statuses = {item["suite"]: item["status"] for item in summary["items"]}
        self.assertEqual(statuses["lm-eval-selected"], "blocked")
        metrics = {item["suite"]: item["metric"] for item in summary["items"]}
        self.assertEqual(metrics["local-bfcl-style-pilot"], "BFCL-style pilot 0.667")
        self.assertEqual(metrics["official-ifeval-pilot"], "prompt strict 0.760")

    def test_markdown_lists_missing_official_suites(self) -> None:
        summary = summarize(build_items("qwen3-4b-strict-toolcall-v4-targeted"), "qwen3-4b-strict-toolcall-v4-targeted", "test-run")
        markdown = render_markdown(summary)

        self.assertIn("official-bfcl", markdown)
        self.assertIn("pilot-only", markdown)
        self.assertIn("local-heldout-strict-tool-call", markdown)

    def test_outputs_are_written_by_cli_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp)
            json_path = output_root / "coverage.json"
            md_path = output_root / "coverage.md"
            summary = summarize(build_items("qwen3-4b-strict-toolcall-v4-targeted"), "qwen3-4b-strict-toolcall-v4-targeted", "test-run")
            json_path.write_text(str(summary), encoding="utf-8")
            md_path.write_text(render_markdown(summary), encoding="utf-8")

            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())


if __name__ == "__main__":
    unittest.main()
