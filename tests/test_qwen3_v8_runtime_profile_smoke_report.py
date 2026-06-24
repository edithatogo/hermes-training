import tempfile
import unittest
from pathlib import Path

from scripts.validate_qwen3_v8_runtime_profile_smoke_report import validate_markdown, validate_payload


class Qwen3V8RuntimeProfileSmokeReportTests(unittest.TestCase):
    def payload(self, root: Path) -> dict:
        raw_summary = root / "raw" / "summary.json"
        best_summary = root / "best" / "summary.json"
        rejected_summary = root / "rejected" / "summary.json"
        for path in (raw_summary, best_summary, rejected_summary):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n", encoding="utf-8")
        residual = [
            "heldout-invalid-tool-handling-payroll",
            "safety-refusal-delete-customer-record",
        ]
        return {
            "candidate": "qwen3-4b-strict-toolcall-v8-wrapper-copy-refusal-repair",
            "status": "runtime-profile-smoke-failed-publication-gate",
            "raw_v8_run": {
                "summary": str(raw_summary),
                "pass_rate": 0.375,
                "empty_think_prefix_cases": 8,
                "residual_strict_failure_ids": residual,
            },
            "runtime_profile_smokes": [
                {
                    "id": "qwen3-v8-runtime-profile-prefill-only-20260624",
                    "summary": str(best_summary),
                    "assistant_prefill": "<think>\n\n</think>\n\n",
                    "pass_rate": 0.75,
                    "json_valid_rate": 1.0,
                    "argument_accuracy_rate": 1.0,
                    "empty_think_prefix_cases": 0,
                    "residual_strict_failure_ids": residual,
                },
                {
                    "id": "qwen3-v8-runtime-profile-prefill-refusal-20260624",
                    "summary": str(rejected_summary),
                    "pass_rate": 0.625,
                    "empty_think_prefix_cases": 0,
                    "residual_strict_failure_count": 3,
                },
            ],
            "blocker_decision": {
                "empty_think_wrapper": "addressed_for_runtime_profile_by_assistant_prefill",
                "raw_model_wrapper_gate": "still_failed_without_runtime_profile",
                "residual_refusal_marker_echo": "still_blocked",
                "publication": "blocked",
            },
            "next_action": "Do not publish v8 weights.",
        }

    def test_validator_records_profile_boundary_and_publication_block(self) -> None:
        with tempfile.TemporaryDirectory(dir="/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety") as tmp:
            failures = validate_payload(self.payload(Path(tmp)), Path("report.json"))
        self.assertEqual(failures, [])

    def test_validator_rejects_publication_or_missing_wrapper_fix(self) -> None:
        with tempfile.TemporaryDirectory(dir="/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety") as tmp:
            payload = self.payload(Path(tmp))
            payload["blocker_decision"]["publication"] = "ready"
            payload["runtime_profile_smokes"][0]["empty_think_prefix_cases"] = 1
            failures = validate_payload(payload, Path("report.json"))
        self.assertIn("publication must remain blocked", failures)
        self.assertIn("assistant-prefill-only smoke must clear empty-think prefixes", failures)

    def test_markdown_keeps_decision_visible(self) -> None:
        failures = validate_markdown(
            "\n".join(
                [
                    "Publication: blocked",
                    "Strict pass rate: `0.750`",
                    "Empty-think prefix cases: `0`",
                    "residual-refusal repair track",
                ]
            )
        )
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
