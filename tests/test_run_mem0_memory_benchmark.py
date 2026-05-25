from __future__ import annotations

import unittest
from unittest.mock import patch

from scripts.run_mem0_memory_benchmark import score_reranked_case


class RunMem0MemoryBenchmarkTests(unittest.TestCase):
    def test_score_reranked_case_uses_wrapper_path_and_scores_result(self) -> None:
        case = {
            "query": "What is the active collection?",
            "expected": {
                "must_retrieve_any": ["mem0_nomic_768"],
                "must_not_retrieve_any": [],
                "top_result_should_contain": "mem0_nomic_768",
            },
        }
        results = [
            {"memory": "The old collection was mem0_old.", "score": 0.9},
            {"memory": "The active collection is mem0_nomic_768.", "score": 0.8},
        ]
        ranked = [
            {"memory": "The active collection is mem0_nomic_768.", "score": 0.8, "rerank_score": 0.99},
            {"memory": "The old collection was mem0_old.", "score": 0.9, "rerank_score": 0.01},
        ]

        with patch("scripts.run_mem0_memory_benchmark.rerank_search_results", return_value=(ranked, 0.125)) as mocked:
            row = score_reranked_case(
                case,
                results,
                "qwen3_causal_lm",
                0.2,
                "Qwen/Qwen3-Reranker-0.6B",
                "cpu",
                4096,
                "Retrieve relevant memory",
                True,
                "http://127.0.0.1:8765",
            )

        self.assertTrue(row["rerank_pass"])
        self.assertTrue(row["rerank_top_result_ok"])
        self.assertEqual(row["rerank_latency_s"], 0.125)
        mocked.assert_called_once()


if __name__ == "__main__":
    unittest.main()
