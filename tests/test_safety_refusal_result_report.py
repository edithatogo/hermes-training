import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_safety_refusal_result_report import build_report, render_markdown
from scripts.validate_safety_refusal_result_report import validate_payload


class SafetyRefusalResultReportTests(unittest.TestCase):
    def write_summary(self, root: Path) -> Path:
        output_dir = root / "standard-benchmarks" / "safety" / "qwen3-v4-peft-safety-refusal-20260616"
        output_dir.mkdir(parents=True)
        summary = {
            "run_id": "qwen3-v4-peft-safety-refusal-20260616",
            "output_dir": str(output_dir),
            "model": "Qwen/Qwen3-4B-MLX-4bit",
            "adapter": "gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter",
            "cases": 8,
            "passed": 1,
            "pass_rate": 0.125,
            "json_valid_rate": 0.0,
            "argument_accuracy_rate": 1.0,
            "empty_think_stripped_pass_rate": 0.5,
            "invalid_tool_handling_rate": 0.2,
            "multi_turn_repair_rate": 0.0,
            "strict_failures_rescued_by_empty_think_strip": 3,
            "strict_failures_rescued_by_empty_think_strip_ids": ["a", "b", "c"],
            "residual_strict_failure_count": 4,
            "residual_strict_failure_ids": ["d", "e", "f", "g"],
            "residual_strict_failure_reasons": {"d": "response contained a forbidden marker"},
        }
        path = output_dir / "summary.json"
        path.write_text(json.dumps(summary), encoding="utf-8")
        return path

    def test_report_preserves_metrics_and_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = build_report(self.write_summary(Path(tmp)))
        self.assertEqual(report["status"], "scored-repair-needed")
        self.assertEqual(report["pass_rate"], 0.125)
        self.assertIn("Do not claim standardized safety/refusal", report["publication_boundary"])
        markdown = render_markdown(report)
        self.assertIn("Strict pass rate: `0.125`", markdown)
        failures = validate_payload(report, Path("report.json"))
        self.assertIn("summary_json must be SSD-backed", "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
