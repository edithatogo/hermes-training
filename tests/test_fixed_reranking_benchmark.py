from __future__ import annotations

import unittest
from unittest.mock import patch

from scripts.run_fixed_reranking_benchmark import lexical_rerank, qwen3_reranker_prompt, rerank_case, xlm_roberta_pair_text


class FixedRerankingBenchmarkTests(unittest.TestCase):
    def test_created_at_rank_fixes_small_recency_margin(self) -> None:
        case = {
            "query": "What is the current preferred local embedding model?",
            "candidates": [
                {
                    "id": "old",
                    "text": "The preferred local embedding model was old-embed-1024.",
                    "score": 0.887,
                    "created_at": "2026-05-24T05:00:00+00:00",
                    "relevant": False,
                },
                {
                    "id": "current",
                    "text": "The current preferred local embedding model is nomic-embed-text.",
                    "score": 0.886,
                    "created_at": "2026-05-24T07:00:00+00:00",
                    "relevant": True,
                },
            ],
        }

        ranked, _ = rerank_case(case, "score_plus_created_at_rank", 0.20, None)

        self.assertEqual(ranked[0]["id"], "current")

    def test_lexical_rerank_prefers_query_overlap(self) -> None:
        ranked = lexical_rerank(
            "Which database stores local metadata?",
            [
                {"id": "runtime", "text": "The runtime endpoint uses llama.cpp.", "score": 0.9, "relevant": False},
                {"id": "sqlite", "text": "SQLite stores local metadata.", "score": 0.5, "relevant": True},
            ],
        )

        self.assertEqual(ranked[0]["id"], "sqlite")

    def test_qwen3_prompt_uses_yes_no_judge_shape(self) -> None:
        prompt = qwen3_reranker_prompt(
            "Which collection is active?",
            "mem0_nomic_768 is the current Qdrant collection.",
            "Retrieve relevant memory",
        )

        self.assertIn('answer can only be "yes" or "no"', prompt)
        self.assertIn("<Query>: Which collection is active?", prompt)
        self.assertIn("<Document>: mem0_nomic_768 is the current Qdrant collection.", prompt)
        self.assertTrue(prompt.endswith("<|im_start|>assistant\n<think>\n\n</think>\n"))

    def test_xlm_roberta_pair_text_uses_reranker_separator_shape(self) -> None:
        pair = xlm_roberta_pair_text("Which collection is active?", "mem0_nomic_768 is active.")

        self.assertEqual(pair, "<s>Which collection is active?</s></s>mem0_nomic_768 is active.</s>")

    def test_mlx_cross_encoder_strategy_delegates_to_mlx_backend(self) -> None:
        case = {
            "query": "Which collection is active?",
            "candidates": [
                {"id": "old", "text": "The old collection was mem0_old.", "score": 0.9, "relevant": False},
                {"id": "current", "text": "The active collection is mem0_nomic_768.", "score": 0.8, "relevant": True},
            ],
        }
        expected = [
            {
                "id": "current",
                "memory": "The active collection is mem0_nomic_768.",
                "text": "The active collection is mem0_nomic_768.",
                "score": 0.8,
                "created_at": None,
                "relevant": True,
                "base_score": 0.8,
                "rerank_score": 1.5,
            },
            {
                "id": "old",
                "memory": "The old collection was mem0_old.",
                "text": "The old collection was mem0_old.",
                "score": 0.9,
                "created_at": None,
                "relevant": False,
                "base_score": 0.9,
                "rerank_score": -1.0,
            },
        ]

        with patch("scripts.run_fixed_reranking_benchmark.mlx_cross_encoder_rerank", return_value=(expected, 0.42)) as mocked:
            ranked, latency = rerank_case(
                case,
                "mlx_cross_encoder",
                0.20,
                "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
                mlx_max_length=512,
            )

        self.assertEqual(ranked[0]["id"], "current")
        self.assertEqual(latency, 0.42)
        mocked.assert_called_once()
        self.assertEqual(mocked.call_args.args[0], "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit")
        self.assertEqual(mocked.call_args.kwargs["max_length"], 512)


if __name__ == "__main__":
    unittest.main()
