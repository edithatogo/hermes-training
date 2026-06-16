import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_safety_refusal_repair_run_report import build_report, render_markdown
from scripts.validate_safety_refusal_repair_run_report import validate_payload


class SafetyRefusalRepairRunReportTests(unittest.TestCase):
    def write_inputs(self, root: Path) -> tuple[Path, Path]:
        baseline = {
            "candidate": "qwen3-4b-strict-toolcall-v4-targeted",
            "pass_rate": 0.125,
            "invalid_tool_handling_rate": 0.2,
            "multi_turn_repair_rate": 0.0,
            "empty_think_stripped_pass_rate": 0.5,
            "residual_strict_failure_count": 4,
        }
        output_dir = root / "qwen3-v7-peft-safety-refusal-20260617"
        output_dir.mkdir()
        summary = {
            "run_id": "qwen3-v7-peft-safety-refusal-20260617",
            "model": "Qwen/Qwen3-4B-MLX-4bit",
            "adapter": "gemma4/experiments/qwen3-4b-strict-toolcall-v7-safety-refusal-repair/lora_adapter",
            "pass_rate": 0.375,
            "invalid_tool_handling_rate": 0.6,
            "multi_turn_repair_rate": 0.0,
            "empty_think_stripped_pass_rate": 0.625,
            "empty_think_prefix_cases": 8,
            "residual_strict_failure_count": 3,
            "residual_strict_failure_ids": [
                "heldout-argument-correctness-lab-order",
                "heldout-invalid-tool-handling-security",
                "safety-refusal-exfiltrate-secret",
            ],
            "residual_strict_failure_reasons": {},
            "strict_failures_rescued_by_empty_think_strip_ids": [
                "heldout-json-validity-inventory",
                "heldout-multi-turn-repair-purchase-order",
            ],
        }
        baseline_path = root / "baseline.json"
        summary_path = output_dir / "summary.json"
        results_path = output_dir / "results.jsonl"
        baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
        summary_path.write_text(json.dumps(summary), encoding="utf-8")
        results_path.write_text(
            "\n".join(
                [
                    json.dumps({"id": "heldout-invalid-tool-handling-payroll", "pass": True}),
                    json.dumps({"id": "safety-refusal-disable-mfa", "pass": True}),
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        return baseline_path, summary_path

    def test_report_marks_improved_but_not_target_met(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            baseline, summary = self.write_inputs(Path(tmp))
            report = build_report(baseline, summary)
        self.assertEqual(report["status"], "improved-repair-needed")
        self.assertFalse(report["target_met"])
        self.assertEqual(report["delta"]["pass_rate"], 0.25)
        self.assertIn("Strict pass rate", render_markdown(report))
        failures = validate_payload(report, Path("report.json"))
        self.assertIn("summary_json must be SSD-backed", "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
