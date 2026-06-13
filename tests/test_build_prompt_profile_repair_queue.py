from __future__ import annotations

import unittest

from scripts.build_prompt_profile_repair_queue import build_rows, command_for, repair_hypothesis


def candidate(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "id": "mlx-community/gemma-4-E4B-it-qat-4bit",
        "family": "gemma",
        "role": "local-runtime",
        "environment": "mac-mlx",
        "parameters": "4B",
        "notes": "",
    }
    data.update(overrides)
    return data


class BuildPromptProfileRepairQueueTests(unittest.TestCase):
    def test_build_rows_keeps_only_strict_format_blockers(self) -> None:
        rows = build_rows(
            [
                candidate(id="repair/model"),
                candidate(id="runtime/model"),
            ],
            [
                {
                    "project": "hermes",
                    "id": "repair/model",
                    "coverage_state": "blocked",
                    "blocked_reason": "blocked by strict Hermes tool-call formatting failure",
                    "evidence": ["reports/example.md"],
                },
                {
                    "project": "hermes",
                    "id": "runtime/model",
                    "coverage_state": "blocked",
                    "blocked_reason": "blocked until runtime artifact/load proof exists",
                },
                {
                    "project": "mem0",
                    "id": "mem0/model",
                    "coverage_state": "blocked",
                    "blocked_reason": "blocked by strict Hermes tool-call formatting failure",
                },
            ],
        )

        self.assertEqual([row["id"] for row in rows], ["repair/model"])
        self.assertEqual(rows[0]["evidence"], ["reports/example.md"])
        self.assertIn("promotion still requires", rows[0]["promotion_boundary"])

    def test_command_for_mlx_candidate_uses_strict_local_scoring(self) -> None:
        command = command_for(candidate(id="Qwen/Qwen3.5-2B", environment="mac-mlx"))

        self.assertIn("scripts/run_local_pilot_benchmark.py", command)
        self.assertIn("No download here", command)
        self.assertIn("--require-no-extra-tool-text", command)
        self.assertIn("--run-id qwen-qwen3-5-2b-prompt-profile-repair", command)

    def test_command_for_endpoint_candidate_uses_endpoint_runner(self) -> None:
        command = command_for(candidate(id="Example/Model-GGUF", environment="mac-lmstudio"))

        self.assertIn("scripts/run_endpoint_pilot_benchmark.py", command)
        self.assertIn("No download here", command)
        self.assertIn("--base-url http://127.0.0.1:<port>/v1", command)
        self.assertIn("--require-no-extra-tool-text", command)

    def test_repair_hypothesis_is_family_specific(self) -> None:
        hypothesis = repair_hypothesis(
            candidate(id="ibm-granite/granite-4.1-3b", family="granite"),
            "blocked by strict Hermes tool-call formatting failure",
        )

        self.assertIn("Granite native tool-call normalization", hypothesis)


if __name__ == "__main__":
    unittest.main()
