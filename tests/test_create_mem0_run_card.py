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

    def test_memory_qwen_rerank_command_includes_model_and_server(self) -> None:
        summary = {
            "run_id": "fixture",
            "tool": "hermes_fixture",
            "suite": "suite.json",
            "rerank_strategy": "qwen3_causal_lm",
            "rerank_model": "Qwen/Qwen3-Reranker-0.6B",
            "qwen3_device": "auto",
            "qwen3_local_files_only": True,
            "qwen3_server_url": "http://127.0.0.1:8765",
        }

        command = "\n".join(command_for_kind("memory+rerank", summary))

        self.assertIn("--rerank-model Qwen/Qwen3-Reranker-0.6B", command)
        self.assertIn("--qwen3-local-files-only", command)
        self.assertIn("--qwen3-server-url http://127.0.0.1:8765", command)
        self.assertIn("--rerank-strategy qwen3_causal_lm", command)

    def test_isolated_fixture_kind_and_command_use_fixture_script(self) -> None:
        summary = {
            "run_id": "fixture",
            "strategy": "qwen3_causal_lm:Qwen/Qwen3-Reranker-0.6B",
            "model": "Qwen/Qwen3-Reranker-0.6B",
            "suite": "suite.json",
            "qwen3_device": "auto",
            "qwen3_max_length": 4096,
            "qwen3_local_files_only": True,
            "qwen3_server_url": "http://127.0.0.1:8765",
            "collection_name": "mem0_fixture_test",
            "top1_accuracy": 1.0,
            "input_count_min": 3,
        }

        self.assertEqual(
            infer_kind(Path("/tmp/mem0-isolated-fixture-rerank/fixture/summary.json"), summary),
            "isolated-fixture-rerank",
        )
        command = "\n".join(command_for_kind("isolated-fixture-rerank", summary))
        decision, reason = decision_for("isolated-fixture-rerank", summary)

        self.assertIn("scripts/run_mem0_isolated_fixture_rerank.py", command)
        self.assertIn("--qwen3-model Qwen/Qwen3-Reranker-0.6B", command)
        self.assertIn("--qwen3-server-url http://127.0.0.1:8765", command)
        self.assertEqual(decision, "keep testing")
        self.assertIn("live add/search multi-result gate", reason)

    def test_isolated_fixture_mlx_command_uses_mlx_flags(self) -> None:
        summary = {
            "run_id": "fixture",
            "strategy": "mlx_cross_encoder:flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
            "model": "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
            "suite": "suite.json",
            "mlx_max_length": 1024,
            "kept_fixture": True,
        }

        command = "\n".join(command_for_kind("isolated-fixture-rerank", summary))

        self.assertIn("--mlx-model flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit", command)
        self.assertIn("--mlx-max-length 1024", command)
        self.assertIn("--keep-fixture", command)
        self.assertNotIn("--qwen3-model flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit", command)


if __name__ == "__main__":
    unittest.main()
