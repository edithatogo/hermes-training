import unittest

from pathlib import Path

from scripts.create_mem0_run_card import command_for_kind, decision_for, infer_kind


class CreateMem0RunCardTests(unittest.TestCase):
    def test_extraction_pass_gate_gets_positive_decision_reason(self) -> None:
        decision, reason = decision_for(
            "extraction",
            {
                "pass_rate": 1.0,
                "json_validity_rate": 1.0,
                "forbidden_hit_rate": 0.0,
                "empty_case_pass_rate": 1.0,
            },
        )

        self.assertEqual(decision, "keep testing")
        self.assertIn("passed the strict JSON", reason)
        self.assertNotIn("did not reach", reason)

    def test_extraction_failure_keeps_fail_closed_reason(self) -> None:
        decision, reason = decision_for(
            "extraction",
            {
                "pass_rate": 0.9,
                "json_validity_rate": 1.0,
                "forbidden_hit_rate": 0.0,
                "empty_case_pass_rate": 1.0,
            },
        )

        self.assertEqual(decision, "keep testing")
        self.assertIn("did not reach", reason)

    def test_reranking_replay_kind_and_command_use_replay_script(self) -> None:
        summary = {
            "run_id": "replay",
            "strategy": "qwen3_causal_lm",
            "model": "Qwen/Qwen3-Reranker-0.6B",
            "suite": "suite.json",
            "qwen3_device": "auto",
            "qwen3_max_length": 4096,
            "qwen3_local_files_only": True,
            "qwen3_server_url": "http://127.0.0.1:8765",
        }

        self.assertEqual(infer_kind(Path("/tmp/mem0-reranking-replay/replay/summary.json"), summary), "reranking-replay")
        command = "\n".join(command_for_kind("reranking-replay", summary))

        self.assertIn("scripts/run_mem0_rerank_replay.py", command)
        self.assertIn("--qwen3-local-files-only", command)
        self.assertIn("--qwen3-server-url http://127.0.0.1:8765", command)


if __name__ == "__main__":
    unittest.main()
