import unittest

from scripts.build_mem0_candidate_queue import blocker_for, queue_priority


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
            "source HF model passed fixed and expanded suites; ONNX bridge still needs runtime proof",
        )


if __name__ == "__main__":
    unittest.main()
