import unittest

from scripts.build_mem0_candidate_queue import blocker_for, command_for, queue_priority


class BuildMem0CandidateQueueTests(unittest.TestCase):
    def test_benchmarked_status_gets_promoted_queue_priority(self) -> None:
        candidate = {
            "id": "BAAI/bge-m3",
            "role": "embedder",
            "status": "benchmarked-cpu-mps-not-promoted",
        }

        self.assertEqual(queue_priority(candidate)[0], 2)
        self.assertEqual(blocker_for(candidate), "benchmarked but not promoted; keep separate collection or artifact")

    def test_source_model_benchmarked_status_gets_promoted_queue_priority(self) -> None:
        candidate = {
            "id": "onnx-community/Qwen3-Reranker-0.6B-ONNX",
            "role": "reranker",
            "status": "source-model-benchmarked",
        }

        self.assertEqual(queue_priority(candidate)[0], 2)
        self.assertEqual(
            blocker_for(candidate),
            "source Qwen/Qwen3-Reranker-0.6B passed suites; ONNX package remains blocked pending bounded CPU/CoreML proof",
        )

    def test_verified_mlx_reranker_records_harness_gap(self) -> None:
        candidate = {
            "id": "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
            "role": "reranker",
            "runtime": ["mlx"],
            "status": "candidate-runtime-id-verified",
        }

        self.assertEqual(queue_priority(candidate)[0], 4)
        self.assertEqual(
            blocker_for(candidate),
            "model repo verified; MLX load/scoring proof is ready before live mem0 integration",
        )
        self.assertIn("--strategy mlx_cross_encoder", command_for(candidate))
        self.assertIn("--mlx-max-length 1024", command_for(candidate))

    def test_fixed_suite_benchmarked_status_records_next_live_gate(self) -> None:
        candidate = {
            "id": "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
            "role": "reranker",
            "runtime": ["mlx"],
            "status": "fixed-suite-benchmarked",
        }

        self.assertEqual(queue_priority(candidate)[0], 2)
        self.assertEqual(
            blocker_for(candidate),
            "fixed suite passed; run expanded replay and isolated fixture before live integration",
        )

    def test_isolated_fixture_proven_status_records_opt_in_boundary(self) -> None:
        candidate = {
            "id": "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
            "role": "reranker",
            "runtime": ["mlx"],
            "status": "isolated-fixture-proven",
        }

        self.assertEqual(queue_priority(candidate)[0], 1)
        self.assertEqual(
            blocker_for(candidate),
            "first bounded cache-hit daily-use probe passed; keep opt-in read mode until broader cold/warm latency proof",
        )
        self.assertIn("run_mem0_read_latency_probe.py", command_for(candidate))
        self.assertIn("--mode mlx-bge", command_for(candidate))
        self.assertIn("--subprocess-read", command_for(candidate))


if __name__ == "__main__":
    unittest.main()
