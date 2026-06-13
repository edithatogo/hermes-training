from __future__ import annotations

import unittest

from scripts.build_runtime_proof_action_queue import build_queue, lane_for, next_command


def candidate(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "id": "example/model",
        "family": "example",
        "role": "local-runtime",
        "environment": "mac-mlx",
        "parameters": "4B",
        "feasibility": "ready",
        "first_runtime": "MLX smoke",
        "notes": "",
    }
    data.update(overrides)
    return data


class RuntimeProofActionQueueTests(unittest.TestCase):
    def test_runtime_support_blocker_gets_distinct_lane(self) -> None:
        item = candidate()

        lane = lane_for(item, "blocked", "blocked by current local runtime support")

        self.assertEqual(lane, "runtime-support-upgrade")

    def test_runtime_support_upgrade_command_avoids_repeat_candidate_run(self) -> None:
        item = candidate(id="google/gemma-4-E2B")

        command = next_command(item, "runtime-support-upgrade")

        self.assertIn("Do not rerun the same candidate", command)
        self.assertNotIn("run_local_pilot_benchmark.py", command)

    def test_runtime_support_upgrade_sorts_after_real_runtime_proofs(self) -> None:
        rows = build_queue(
            [
                candidate(id="blocked/runtime", environment="hf-transformers"),
                candidate(id="missing/artifact", environment="mac-mlx", feasibility="needs-runtime-proof"),
            ],
            [
                {
                    "project": "hermes",
                    "id": "blocked/runtime",
                    "coverage_state": "blocked",
                    "blocked_reason": "blocked by current local runtime support",
                },
                {
                    "project": "hermes",
                    "id": "missing/artifact",
                    "coverage_state": "blocked",
                    "blocked_reason": "blocked until runtime artifact/load proof exists",
                },
            ],
        )

        self.assertEqual(rows[0]["id"], "missing/artifact")
        self.assertEqual(rows[1]["lane"], "runtime-support-upgrade")


if __name__ == "__main__":
    unittest.main()
