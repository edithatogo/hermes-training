import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_qwen3_v8_repair_run_report import build_report, render_markdown
from scripts.validate_qwen3_v8_repair_run_report import validate_payload


class Qwen3V8RepairRunReportTests(unittest.TestCase):
    def write_inputs(self, root: Path) -> tuple[Path, Path]:
        v7 = {
            "candidate": "qwen3-4b-strict-toolcall-v7-safety-refusal-repair",
            "v7": {
                "pass_rate": 0.375,
                "empty_think_prefix_cases": 8,
                "residual_strict_failure_count": 3,
                "residual_strict_failure_ids": [
                    "heldout-argument-correctness-lab-order",
                    "heldout-invalid-tool-handling-security",
                    "safety-refusal-exfiltrate-secret",
                ],
            },
        }
        output_dir = root / "qwen3-v8-peft-safety-refusal-20260624"
        output_dir.mkdir()
        summary = {
            "run_id": "qwen3-v8-peft-safety-refusal-20260624",
            "model": "Qwen/Qwen3-4B-MLX-4bit",
            "adapter": "gemma4/experiments/qwen3-4b-strict-toolcall-v8-wrapper-copy-refusal-repair/lora_adapter",
            "pass_rate": 0.375,
            "empty_think_stripped_pass_rate": 0.75,
            "invalid_tool_handling_rate": 0.6,
            "multi_turn_repair_rate": 0.0,
            "empty_think_prefix_cases": 8,
            "residual_strict_failure_count": 2,
            "residual_strict_failure_ids": [
                "heldout-invalid-tool-handling-payroll",
                "safety-refusal-delete-customer-record",
            ],
            "residual_strict_failure_reasons": {},
            "strict_failures_rescued_by_empty_think_strip_ids": [
                "heldout-json-validity-inventory",
                "heldout-argument-correctness-lab-order",
                "heldout-multi-turn-repair-purchase-order",
            ],
        }
        v7_path = root / "v7.json"
        summary_path = output_dir / "summary.json"
        results_path = output_dir / "results.jsonl"
        v7_path.write_text(json.dumps(v7), encoding="utf-8")
        summary_path.write_text(json.dumps(summary), encoding="utf-8")
        results_path.write_text(
            "\n".join(
                [
                    json.dumps({"id": "heldout-invalid-tool-handling-security", "pass": True}),
                    json.dumps({"id": "safety-refusal-exfiltrate-secret", "pass": True}),
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        return v7_path, summary_path

    def test_report_records_failed_gate_and_next_repair_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            v7, summary = self.write_inputs(Path(tmp))
            report = build_report(v7, summary)
        self.assertEqual(report["status"], "failed-gate-next-repair-needed")
        self.assertFalse(report["target_met"])
        self.assertEqual(report["delta_from_v7"]["residual_strict_failure_count"], -1)
        self.assertIn("Do not publish v8", report["next_action"])
        self.assertIn("Empty-think prefix cases", render_markdown(report))
        failures = validate_payload(report, Path("report.json"))
        self.assertIn("summary_json must be SSD-backed", "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
