from __future__ import annotations

import argparse
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.mem0_read import cache_key, load_cache, run_guarded_read, select_strategy


class Mem0ReadTests(unittest.TestCase):
    def build_args(self, **overrides: object) -> argparse.Namespace:
        values = {
            "query": "active collection",
            "tool": "cmd",
            "mode": "close-margin",
            "timeout_s": 120.0,
            "recency_weight": 0.2,
            "model": "Qwen/Qwen3-Reranker-0.6B",
            "qwen3_device": "auto",
            "qwen3_max_length": 4096,
            "qwen3_instruction": "Retrieve relevant memory",
            "qwen3_local_files_only": False,
            "qwen3_server_url": None,
            "mlx_max_length": 1024,
            "fallback_to_vector": False,
            "include_raw": False,
            "cache_path": None,
            "cache_ttl_s": 0.0,
            "refresh_cache": False,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_select_strategy_defaults_to_close_margin(self) -> None:
        self.assertEqual(select_strategy("close-margin"), "score_plus_created_at_rank_close_margin")
        self.assertEqual(select_strategy("vector"), "vector")
        self.assertEqual(select_strategy("qwen3"), "qwen3_causal_lm")
        self.assertEqual(select_strategy("mlx-bge"), "mlx_cross_encoder")

    def test_guarded_read_uses_close_margin_by_default(self) -> None:
        args = self.build_args()
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
        self.assertFalse(output["mem0_cache_hit"])
        self.assertEqual(output["results"], ranked)
        search.assert_called_once_with("cmd", "active collection", 120.0)
        rerank.assert_called_once()

    def test_guarded_read_can_use_default_mlx_bge_model(self) -> None:
        args = self.build_args(mode="mlx-bge")
        results = [{"memory": "The active collection is mem0_nomic_768.", "score": 0.9}]
        ranked = [dict(results[0], rerank_score=0.99)]

        with (
            patch("scripts.mem0_read.run_mem0_search", return_value=(results, "raw", 1.2)),
            patch("scripts.mem0_read.rerank_search_results", return_value=(ranked, 0.14)) as rerank,
        ):
            output = run_guarded_read(args)

        self.assertEqual(output["strategy"], "mlx_cross_encoder")
        self.assertEqual(output["model"], "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit")
        self.assertEqual(output["rerank_latency_s"], 0.14)
        self.assertEqual(rerank.call_args.args[4], "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit")
        self.assertEqual(rerank.call_args.args[10], 1024)

    def test_guarded_read_can_fallback_to_vector(self) -> None:
        args = self.build_args(
            mode="qwen3",
            qwen3_local_files_only=True,
            qwen3_server_url="http://127.0.0.1:8765",
            fallback_to_vector=True,
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

    def test_search_cache_miss_writes_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            args = self.build_args(cache_path=cache_path, cache_ttl_s=60.0)
            results = [{"memory": "The active collection is mem0_nomic_768.", "score": 0.9}]
            ranked = [dict(results[0], rerank_score=0.9)]

            with (
                patch("scripts.mem0_read.run_mem0_search", return_value=(results, "raw", 1.2)),
                patch("scripts.mem0_read.rerank_search_results", return_value=(ranked, 0.01)),
            ):
                output = run_guarded_read(args)

            cache = load_cache(cache_path)

        self.assertFalse(output["mem0_cache_hit"])
        self.assertEqual(output["cache_path"], str(cache_path))
        self.assertEqual(len(cache["entries"]), 1)

    def test_search_cache_hit_skips_mem0_but_reranks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            args = self.build_args(cache_path=cache_path, cache_ttl_s=60.0)
            key = cache_key(args)
            results = [{"memory": "The active collection is mem0_nomic_768.", "score": 0.9}]
            cache_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "entries": {
                            key: {
                                "cached_at": time.time(),
                                "results": results,
                                "raw": "raw",
                                "source_mem0_search_latency_s": 1.2,
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            ranked = [dict(results[0], rerank_score=0.9)]

            with (
                patch("scripts.mem0_read.run_mem0_search") as search,
                patch("scripts.mem0_read.rerank_search_results", return_value=(ranked, 0.01)) as rerank,
            ):
                output = run_guarded_read(args)

        search.assert_not_called()
        rerank.assert_called_once()
        self.assertTrue(output["mem0_cache_hit"])
        self.assertEqual(output["mem0_search_latency_s"], 0.0)
        self.assertEqual(output["source_mem0_search_latency_s"], 1.2)

    def test_cache_ttl_zero_disables_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            args = self.build_args(cache_path=cache_path, cache_ttl_s=0.0)
            results = [{"memory": "The active collection is mem0_nomic_768.", "score": 0.9}]

            with (
                patch("scripts.mem0_read.run_mem0_search", return_value=(results, "raw", 1.2)) as search,
                patch("scripts.mem0_read.rerank_search_results", return_value=(results, 0.0)),
            ):
                run_guarded_read(args)

        search.assert_called_once()
        self.assertFalse(cache_path.exists())

    def test_corrupt_cache_file_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            cache_path.write_text("not json", encoding="utf-8")
            args = self.build_args(cache_path=cache_path, cache_ttl_s=60.0)
            results = [{"memory": "The active collection is mem0_nomic_768.", "score": 0.9}]

            with (
                patch("scripts.mem0_read.run_mem0_search", return_value=(results, "raw", 1.2)),
                patch("scripts.mem0_read.rerank_search_results", return_value=(results, 0.0)),
            ):
                output = run_guarded_read(args)

        self.assertFalse(output["mem0_cache_hit"])
        self.assertEqual(load_cache(cache_path)["version"], 1)


if __name__ == "__main__":
    unittest.main()
