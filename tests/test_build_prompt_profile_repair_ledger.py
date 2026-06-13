from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts.build_prompt_profile_repair_ledger import build_ledger, candidate_status


def queue_row(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "id": "Qwen/Qwen3.5-2B",
        "environment": "mac-mlx",
        "blocked_reason": "blocked by empty/no-content generation under the strict prompt",
    }
    data.update(overrides)
    return data


class BuildPromptProfileRepairLedgerTests(unittest.TestCase):
    def test_non_local_candidate_is_blocked_without_experiments(self) -> None:
        row = queue_row(id="Qwen/Qwen3.6-35B-A3B", environment="azure-cuda")

        status, next_action = candidate_status(row, [])

        self.assertEqual(status, "blocked-non-local")
        self.assertIn("cloud/offload", next_action)

    def test_local_candidate_with_analysis_variant_gets_distinct_status(self) -> None:
        status, next_action = candidate_status(
            queue_row(id="ibm-granite/granite-4.1-3b", environment="mac-mlx"),
            [{"variant": "granite-native-normalizer-analysis", "raw_output_promotion_allowed": False}],
        )

        self.assertEqual(status, "pending-local-with-analysis-variant")
        self.assertIn("analysis-only", next_action)

    def test_build_ledger_keeps_all_queue_rows_and_records_results(self) -> None:
        rows = build_ledger(
            [
                queue_row(id="Qwen/Qwen3.5-2B", environment="mac-mlx"),
                queue_row(id="Qwen/Qwen3.6-35B-A3B", environment="azure-cuda"),
            ],
            [
                {
                    "candidate": "Qwen/Qwen3.5-2B",
                    "variant": "strict-suffix-copy-exact",
                    "runner": "local",
                    "raw_output_promotion_allowed": True,
                    "strict_scoring": True,
                    "priority": 1,
                }
            ],
            [
                {
                    "candidate": "Qwen/Qwen3.5-2B",
                    "variant": "strict-suffix-copy-exact",
                    "status": "completed-no-promotion",
                    "next_action": "try another variant",
                    "result_report": "reports/benchmark/local-pilots/example.md",
                    "source_summary": "/tmp/example/summary.json",
                    "pass_rate": 0.0,
                }
            ],
        )

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["status"], "completed-no-promotion")
        self.assertEqual(rows[0]["result_report"], "reports/benchmark/local-pilots/example.md")
        self.assertEqual(rows[0]["pass_rate"], 0.0)
        self.assertEqual(rows[1]["status"], "blocked-non-local")
        self.assertEqual(rows[1]["experiments"], [])

    def test_build_ledger_keeps_best_result_and_latest_next_action(self) -> None:
        rows = build_ledger(
            [queue_row(id="Qwen/Qwen3.5-0.8B", environment="mac-mlx")],
            [
                {
                    "candidate": "Qwen/Qwen3.5-0.8B",
                    "variant": "strict-suffix-copy-exact",
                    "runner": "local",
                    "raw_output_promotion_allowed": True,
                    "strict_scoring": True,
                    "priority": 1,
                },
                {
                    "candidate": "Qwen/Qwen3.5-0.8B",
                    "variant": "qwen-no-think-prefill",
                    "runner": "local",
                    "raw_output_promotion_allowed": True,
                    "strict_scoring": True,
                    "priority": 2,
                },
                {
                    "candidate": "Qwen/Qwen3.5-0.8B",
                    "variant": "empty-output-retry",
                    "runner": "local",
                    "raw_output_promotion_allowed": True,
                    "strict_scoring": True,
                    "priority": 3,
                },
            ],
            [
                {
                    "candidate": "Qwen/Qwen3.5-0.8B",
                    "variant": "strict-suffix-copy-exact",
                    "status": "completed-no-promotion",
                    "next_action": "try another variant",
                    "result_report": "reports/benchmark/local-pilots/strict.md",
                    "source_summary": "/tmp/strict/summary.json",
                    "pass_rate": 0.5,
                },
                {
                    "candidate": "Qwen/Qwen3.5-0.8B",
                    "variant": "qwen-no-think-prefill",
                    "status": "completed-no-promotion",
                    "next_action": "try empty output retry",
                    "result_report": "reports/benchmark/local-pilots/no-think.md",
                    "source_summary": "/tmp/no-think/summary.json",
                    "pass_rate": 0.25,
                },
                {
                    "candidate": "Qwen/Qwen3.5-0.8B",
                    "variant": "empty-output-retry",
                    "status": "completed-no-promotion",
                    "next_action": "stop prompt-only repairs",
                    "result_report": "reports/benchmark/local-pilots/empty.md",
                    "source_summary": "/tmp/empty/summary.json",
                    "pass_rate": 0.0,
                },
            ],
        )

        self.assertEqual(rows[0]["result_report"], "reports/benchmark/local-pilots/strict.md")
        self.assertEqual(rows[0]["pass_rate"], 0.5)
        self.assertEqual(rows[0]["next_action"], "stop prompt-only repairs")
        self.assertEqual(
            rows[0]["completed_variants"],
            ["strict-suffix-copy-exact", "qwen-no-think-prefill", "empty-output-retry"],
        )
        self.assertEqual(
            rows[0]["result_reports"],
            [
                "reports/benchmark/local-pilots/strict.md",
                "reports/benchmark/local-pilots/no-think.md",
                "reports/benchmark/local-pilots/empty.md",
            ],
        )


if __name__ == "__main__":
    unittest.main()
