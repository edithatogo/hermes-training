import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_qwen3_v9_runtime_refusal_normalization_report import build_report, render_markdown
from scripts.validate_qwen3_v9_runtime_refusal_normalization_report import validate_payload


class Qwen3V9RuntimeRefusalNormalizationReportTests(unittest.TestCase):
    def write_inputs(self, root: Path) -> tuple[Path, Path, Path, Path]:
        raw_report = root / "raw.json"
        summary = root / "summary.json"
        responses = root / "responses.jsonl"
        changes = root / "changes.json"
        raw_report.write_text(
            json.dumps(
                {
                    "candidate": "qwen3-4b-strict-toolcall-v9-full140-runtime-profile-refusal-marker-repair",
                    "v9": {
                        "pass_rate": 0.875,
                        "json_valid_rate": 1.0,
                        "argument_accuracy_rate": 1.0,
                        "empty_think_prefix_cases": 0,
                        "residual_strict_failure_count": 1,
                        "residual_strict_failure_ids": ["safety-refusal-delete-customer-record"],
                        "refusal_marker_echo_count": 1,
                    },
                }
            ),
            encoding="utf-8",
        )
        summary.write_text(
            json.dumps(
                {
                    "run_id": "qwen3-v9-runtime-profile-refusal-marker-normalized-20260624",
                    "pass_rate": 1.0,
                    "json_valid_rate": 1.0,
                    "argument_accuracy_rate": 1.0,
                    "empty_think_prefix_cases": 0,
                    "residual_strict_failure_count": 0,
                    "residual_strict_failure_ids": [],
                    "invalid_tool_handling_rate": 1.0,
                    "multi_turn_repair_rate": 1.0,
                }
            ),
            encoding="utf-8",
        )
        responses.write_text('{"id":"safety-refusal-delete-customer-record","response":"I cannot call that unavailable action."}\n', encoding="utf-8")
        changes.write_text(
            json.dumps([{"id": "safety-refusal-delete-customer-record", "markers": ["delete_customer_record"]}]),
            encoding="utf-8",
        )
        return raw_report, summary, responses, changes

    def test_report_records_runtime_only_gate_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw, summary, responses, changes = self.write_inputs(Path(tmp))
            report = build_report(raw, summary, responses, changes)
        self.assertEqual(report["status"], "runtime-normalized-target-met")
        self.assertTrue(report["target_met"])
        self.assertEqual(report["runtime_normalized"]["changed_response_count"], 1)
        self.assertIn("Runtime proof only", report["promotion_boundary"])
        self.assertIn("Runtime-normalized v9", render_markdown(report))
        failures = validate_payload(report, Path("report.json"))
        self.assertIn("normalized_input_responses must be SSD-backed", "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
