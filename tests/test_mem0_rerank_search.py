from __future__ import annotations

import unittest
from unittest.mock import patch

from scripts.mem0_rerank_search import rerank_search_results


class Mem0RerankSearchTests(unittest.TestCase):
    def test_empty_results_do_not_load_qwen_model(self) -> None:
        with patch("scripts.mem0_rerank_search.qwen3_causal_lm_rerank") as mocked:
            ranked, latency = rerank_search_results(
                "missing memory",
                [],
                "qwen3_causal_lm",
                0.20,
                "Qwen/Qwen3-Reranker-0.6B",
                "auto",
                4096,
                "Retrieve relevant memory",
            )

        self.assertEqual(ranked, [])
        self.assertEqual(latency, 0.0)
        mocked.assert_not_called()

    def test_qwen3_strategy_requires_model(self) -> None:
        with self.assertRaisesRegex(ValueError, "--model is required"):
            rerank_search_results(
                "active mem0 collection",
                [{"memory": "The active collection is mem0_nomic_768.", "score": 0.9}],
                "qwen3_causal_lm",
                0.20,
                None,
                "auto",
                4096,
                "Retrieve relevant memory",
            )

    def test_qwen3_strategy_delegates_to_causal_lm_reranker(self) -> None:
        results = [
            {"memory": "Old collection was mem0_old.", "score": 0.91},
            {"memory": "Current collection is mem0_nomic_768.", "score": 0.88},
        ]
        expected = [dict(results[1], rerank_score=0.99), dict(results[0], rerank_score=0.1)]

        with patch("scripts.mem0_rerank_search.qwen3_causal_lm_rerank", return_value=(expected, 0.123)) as mocked:
            ranked, latency = rerank_search_results(
                "What is the active mem0 collection?",
                results,
                "qwen3_causal_lm",
                0.20,
                "Qwen/Qwen3-Reranker-0.6B",
                "cpu",
                4096,
                "Retrieve relevant memory",
            )

        self.assertEqual(ranked, expected)
        self.assertEqual(latency, 0.123)
        mocked.assert_called_once_with(
            "Qwen/Qwen3-Reranker-0.6B",
            "What is the active mem0 collection?",
            results,
            "cpu",
            4096,
            "Retrieve relevant memory",
        )


if __name__ == "__main__":
    unittest.main()
