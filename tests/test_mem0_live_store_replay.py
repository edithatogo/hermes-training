from __future__ import annotations

import unittest

from scripts.run_mem0_live_store_replay import aggregate, compare_case, normalize_results, render_report, text_hash


class Mem0LiveStoreReplayTests(unittest.TestCase):
    def test_normalize_results_accepts_wrapper_shapes(self) -> None:
        rows = [{"memory": "alpha"}, {"memory": "beta"}]

        self.assertEqual(normalize_results(rows), rows)
        self.assertEqual(normalize_results({"results": rows}), rows)
        self.assertEqual(normalize_results({"results": ["skip", rows[0]]}), [rows[0]])
        self.assertEqual(normalize_results({"unexpected": rows}), [])

    def test_aggregate_scores_only_comparable_cases(self) -> None:
        metrics = aggregate(
            [
                {
                    "default_count": 1,
                    "top1_match": True,
                    "default_top_recall_at_candidate_k": True,
                    "overlap_at_candidate_k": 2,
                },
                {
                    "default_count": 0,
                    "top1_match": False,
                    "default_top_recall_at_candidate_k": False,
                    "overlap_at_candidate_k": 0,
                },
            ]
        )

        self.assertEqual(metrics["comparable_cases"], 1)
        self.assertEqual(metrics["top1_match_rate"], 1.0)
        self.assertEqual(metrics["default_top_recall_rate"], 1.0)
        self.assertEqual(metrics["mean_overlap_at_k"], 2.0)

    def test_compare_case_matches_candidate_metadata_source_hash(self) -> None:
        source_hash = "source-hash-1"
        case = compare_case(
            "q01",
            [{"memory": "original", "metadata": {"source_hash": source_hash}}],
            [{"memory": "copied text", "metadata": {"source_hash": source_hash}}],
        )

        self.assertTrue(case["top1_match"])
        self.assertTrue(case["default_top_recall_at_candidate_k"])

    def test_render_report_excludes_raw_memory_text(self) -> None:
        private_text = "This raw private memory must not appear in committed markdown."
        private_hash = text_hash(private_text)
        summary = {
            "run_id": "test-run",
            "created_at": "2026-06-13T00:00:00+00:00",
            "query_count": 1,
            "unique_memory_count": 1,
            "candidate_collection": "mem0_embeddinggemma_300m_768_test",
            "candidate_config_path": "/Volumes/PortableSSD/private/config.json",
            "private_raw_export_path": "/Volumes/PortableSSD/private/default.jsonl",
            "private_candidate_search_path": "/Volumes/PortableSSD/private/candidate.jsonl",
            "summary_json_path": "/Volumes/PortableSSD/private/summary.json",
            "metrics": {
                "comparable_cases": 1,
                "top1_match_rate": 1.0,
                "default_top_recall_rate": 1.0,
                "mean_overlap_at_k": 1.0,
            },
            "cases": [
                {
                    "query_id": "q01",
                    "default_count": 1,
                    "candidate_count": 1,
                    "top1_match": True,
                    "default_top_recall_at_candidate_k": True,
                    "default_top_hash": private_hash,
                    "candidate_top_hash": private_hash,
                }
            ],
            "decision": "keep opt-in",
        }

        report = render_report(summary)

        self.assertNotIn(private_text, report)
        self.assertIn(private_hash[:12], report)
        self.assertIn("Private raw export", report)


if __name__ == "__main__":
    unittest.main()
