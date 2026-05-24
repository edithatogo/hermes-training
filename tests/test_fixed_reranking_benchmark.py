from __future__ import annotations

import unittest

from scripts.run_fixed_reranking_benchmark import lexical_rerank, rerank_case


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


if __name__ == "__main__":
    unittest.main()
