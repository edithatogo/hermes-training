from __future__ import annotations

import unittest

from scripts.run_mem0_live_store_rerank_replay import evaluate_strategy, render_report, rows_by_query


class Mem0LiveStoreRerankReplayTests(unittest.TestCase):
    def test_evaluate_strategy_uses_source_hash_without_raw_text_in_report(self) -> None:
        default_rows = rows_by_query(
            [
                {
                    "query_id": "q01",
                    "rank": 1,
                    "hash": "default-top-hash",
                    "raw": {"memory": "private default top"},
                }
            ]
        )
        candidate_rows = rows_by_query(
            [
                {
                    "query_id": "q01",
                    "rank": 1,
                    "hash": "other-hash",
                    "raw": {
                        "memory": "unrelated candidate",
                        "score": 0.9,
                        "metadata": {"source_hash": "other-hash"},
                    },
                },
                {
                    "query_id": "q01",
                    "rank": 2,
                    "hash": "default-top-hash",
                    "raw": {
                        "memory": "default top candidate",
                        "score": 0.8,
                        "metadata": {"source_hash": "default-top-hash"},
                    },
                },
            ]
        )

        result = evaluate_strategy("vector", default_rows, candidate_rows, 0.2)

        self.assertEqual(result["metrics"]["top1_match_rate"], 0.0)
        self.assertEqual(result["metrics"]["default_top_recall_rate"], 1.0)
        self.assertEqual(result["cases"][0]["default_top_rank"], 2)

        report = render_report(
            {
                "run_id": "test",
                "created_at": "2026-06-13T00:00:00+00:00",
                "strategy_results": [result],
                "best_strategy": "vector",
                "best_cases": result["cases"],
                "default_results_path": "/private/default.jsonl",
                "candidate_results_path": "/private/candidate.jsonl",
                "summary_json_path": "/private/summary.json",
                "decision": "No raw text.",
            }
        )
        self.assertIn("default-top", report)
        self.assertNotIn("private default top", report)
        self.assertNotIn("default top candidate", report)


if __name__ == "__main__":
    unittest.main()
