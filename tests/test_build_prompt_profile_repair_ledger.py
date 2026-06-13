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


if __name__ == "__main__":
    unittest.main()
