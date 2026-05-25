from __future__ import annotations

import argparse
import unittest
from unittest.mock import patch

from scripts.mem0_read import run_guarded_read, select_strategy


class Mem0ReadTests(unittest.TestCase):
    def test_select_strategy_defaults_to_close_margin(self) -> None:
        self.assertEqual(select_strategy("close-margin"), "score_plus_created_at_rank_close_margin")
        self.assertEqual(select_strategy("vector"), "vector")
        self.assertEqual(select_strategy("qwen3"), "qwen3_causal_lm")

    def test_guarded_read_uses_close_margin_by_default(self) -> None:
        args = argparse.Namespace(
            query="active collection",
            tool="cmd",
            mode="close-margin",
            timeout_s=120.0,
            recency_weight=0.2,
            model="Qwen/Qwen3-Reranker-0.6B",
            qwen3_device="auto",
            qwen3_max_length=4096,
            qwen3_instruction="Retrieve relevant memory",
            qwen3_local_files_only=False,
            qwen3_server_url=None,
            fallback_to_vector=False,
            include_raw=False,
        )
        results = [{"memory": "The active collection is mem0_nomic_768.", "score": 0.9}]
        ranked = [dict(results[0], rerank_score=0.9)]

        with (
            patch("scripts.mem0_read.run_mem0_search", return_value=(results, "raw", 1.2)) as search,
            patch("scripts.mem0_read.rerank_search_results", return_value=(ranked, 0.01)) as rerank,
        ):
            output = run_guarded_read(args)

        self.assertTrue(output["read_only"])
        self.assertFalse(output["mutates_mem0_config"])
        self.assertEqual(output["strategy"], "score_plus_created_at_rank_close_margin")
        self.assertEqual(output["results"], ranked)
        search.assert_called_once_with("cmd", "active collection", 120.0)
        rerank.assert_called_once()

    def test_guarded_read_can_fallback_to_vector(self) -> None:
        args = argparse.Namespace(
            query="active collection",
            tool="cmd",
            mode="qwen3",
            timeout_s=120.0,
            recency_weight=0.2,
            model="Qwen/Qwen3-Reranker-0.6B",
            qwen3_device="auto",
            qwen3_max_length=4096,
            qwen3_instruction="Retrieve relevant memory",
            qwen3_local_files_only=True,
            qwen3_server_url="http://127.0.0.1:8765",
            fallback_to_vector=True,
            include_raw=False,
        )
        results = [{"memory": "The active collection is mem0_nomic_768.", "score": 0.9}]

        with (
            patch("scripts.mem0_read.run_mem0_search", return_value=(results, "raw", 1.2)),
            patch(
                "scripts.mem0_read.rerank_search_results",
                side_effect=[RuntimeError("service down"), (results, 0.0)],
            ),
        ):
            output = run_guarded_read(args)

        self.assertEqual(output["strategy"], "vector")
        self.assertIn("service down", output["fallback_reason"])
        self.assertEqual(output["model"], "")


if __name__ == "__main__":
    unittest.main()
