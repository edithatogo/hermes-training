from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.run_mem0_rerank_replay import (
    evaluate_case,
    load_suite,
    suite_candidates_to_mem0_results,
    summarize_rows,
)


class RunMem0RerankReplayTests(unittest.TestCase):
    def test_suite_candidates_to_mem0_results_preserves_relevance_and_scores(self) -> None:
        case = {
            "candidates": [
                {
                    "id": "current",
                    "text": "The current collection is mem0_nomic_768.",
                    "score": 0.88,
                    "created_at": "2026-05-24T07:00:00+00:00",
                    "relevant": True,
                }
            ]
        }

        results = suite_candidates_to_mem0_results(case)

        self.assertEqual(
            results,
            [
                {
                    "id": "current",
                    "memory": "The current collection is mem0_nomic_768.",
                    "text": "The current collection is mem0_nomic_768.",
                    "score": 0.88,
                    "created_at": "2026-05-24T07:00:00+00:00",
                    "relevant": True,
                }
            ],
        )

    def test_evaluate_case_uses_wrapper_rerank_path(self) -> None:
        case = {
            "id": "collection",
            "category": "recency_conflict",
            "query": "What is the active collection?",
            "candidates": [
                {"id": "old", "text": "The old collection was mem0_old.", "score": 0.9, "relevant": False},
                {"id": "new", "text": "The active collection is mem0_nomic_768.", "score": 0.8, "relevant": True},
            ],
        }
        ranked = [
            {"id": "new", "memory": "The active collection is mem0_nomic_768.", "score": 0.8, "rerank_score": 0.99, "relevant": True},
            {"id": "old", "memory": "The old collection was mem0_old.", "score": 0.9, "rerank_score": 0.01, "relevant": False},
        ]

        with patch("scripts.run_mem0_rerank_replay.rerank_search_results", return_value=(ranked, 0.123)) as mocked:
            row = evaluate_case(
                case,
                "qwen3_causal_lm",
                0.20,
                "Qwen/Qwen3-Reranker-0.6B",
                "cpu",
                4096,
                "Retrieve relevant memory",
                True,
                "http://127.0.0.1:8765",
            )

        self.assertEqual(row["top_candidate_id"], "new")
        self.assertTrue(row["top1_pass"])
        self.assertEqual(row["rerank_latency_s"], 0.123)
        mocked.assert_called_once()

    def test_summarize_rows_calculates_core_metrics(self) -> None:
        rows = [
            {
                "id": "a",
                "category": "recency_conflict",
                "top1_pass": True,
                "reciprocal_rank": 1.0,
                "ndcg_at_3": 1.0,
                "recall_at_3": 1.0,
                "rerank_latency_s": 0.1,
            },
            {
                "id": "b",
                "category": "distractor_resistance",
                "top1_pass": False,
                "reciprocal_rank": 0.5,
                "ndcg_at_3": 0.75,
                "recall_at_3": 1.0,
                "rerank_latency_s": 0.3,
            },
        ]

        summary = summarize_rows(
            rows,
            "run",
            Path("suite.json"),
            Path("/tmp/out"),
            "qwen3_causal_lm",
            0.2,
            "Qwen/Qwen3-Reranker-0.6B",
            "cpu",
            4096,
            "Retrieve relevant memory",
            True,
            "http://127.0.0.1:8765",
        )

        self.assertEqual(summary["top1_accuracy"], 0.5)
        self.assertEqual(summary["recall_at_3"], 1.0)
        self.assertEqual(summary["recency_conflict_pass_rate"], 1.0)
        self.assertEqual(summary["distractor_resistance_pass_rate"], 0.0)
        self.assertEqual(summary["rerank_latency_p50_s"], 0.2)
        self.assertEqual(summary["qwen3_server_url"], "http://127.0.0.1:8765")

    def test_load_suite_rejects_single_candidate_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "suite.json"
            path.write_text(
                '[{"id":"bad","category":"direct_recall","query":"q","candidates":[{"id":"a","text":"x","relevant":true}]}]',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "at least two"):
                load_suite(path)


if __name__ == "__main__":
    unittest.main()
