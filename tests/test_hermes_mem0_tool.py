from __future__ import annotations

import argparse
import contextlib
import io
import json
import unittest
from unittest.mock import patch

from scripts.hermes_mem0_tool import build_read_args, load_payload, main, render_tool_result


class HermesMem0ToolTests(unittest.TestCase):
    def test_load_payload_uses_query_argument(self) -> None:
        self.assertEqual(load_payload('{"query":"stdin"}', "arg"), {"query": "arg"})

    def test_build_read_args_defaults_to_cached_close_margin(self) -> None:
        cli_args = argparse.Namespace(
            tool="cmd",
            mode="close-margin",
            cache_path=None,
            cache_ttl_s=300.0,
            refresh_cache=False,
            timeout_s=120.0,
            recency_weight=0.2,
            include_raw=False,
            fallback_to_vector=False,
            model="Qwen/Qwen3-Reranker-0.6B",
            qwen3_device="auto",
            qwen3_max_length=4096,
            qwen3_local_files_only=False,
            qwen3_server_url=None,
            mlx_max_length=1024,
            qwen3_instruction="Retrieve",
        )

        read_args = build_read_args(cli_args, {"query": "active collection"})

        self.assertEqual(read_args.query, "active collection")
        self.assertEqual(read_args.mode, "close-margin")
        self.assertEqual(read_args.cache_ttl_s, 300.0)
        self.assertFalse(read_args.refresh_cache)

    def test_build_read_args_defaults_mlx_bge_model_for_mlx_mode(self) -> None:
        cli_args = argparse.Namespace(
            tool="cmd",
            mode="close-margin",
            cache_path=None,
            cache_ttl_s=300.0,
            refresh_cache=False,
            timeout_s=120.0,
            recency_weight=0.2,
            include_raw=False,
            fallback_to_vector=False,
            model="Qwen/Qwen3-Reranker-0.6B",
            qwen3_device="auto",
            qwen3_max_length=4096,
            qwen3_local_files_only=False,
            qwen3_server_url=None,
            qwen3_instruction="Retrieve",
            mlx_max_length=1024,
        )

        read_args = build_read_args(cli_args, {"query": "active collection", "mode": "mlx-bge"})

        self.assertEqual(read_args.mode, "mlx-bge")
        self.assertEqual(read_args.model, "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit")
        self.assertEqual(read_args.mlx_max_length, 1024)

    def test_render_tool_result_filters_to_agent_contract(self) -> None:
        output = render_tool_result(
            {
                "query": "q",
                "mode": "close-margin",
                "strategy": "score_plus_created_at_rank_close_margin",
                "mem0_cache_hit": True,
                "input_count": 1,
                "total_latency_s": 0.0,
                "mem0_search_latency_s": 0.0,
                "rerank_latency_s": 0.0,
                "results": [
                    {
                        "id": "1",
                        "memory": "active collection is mem0_nomic_768",
                        "score": 0.9,
                        "rerank_score": 1.0,
                        "created_at": "2026-05-26T00:00:00Z",
                        "metadata": {"source": "test"},
                        "raw_extra": "omitted",
                    }
                ],
            }
        )

        self.assertTrue(output["ok"])
        self.assertTrue(output["read_only"])
        self.assertEqual(output["tool"], "hermes_mem0_read")
        self.assertEqual(output["memories"][0]["memory"], "active collection is mem0_nomic_768")
        self.assertNotIn("raw_extra", output["memories"][0])

    def test_main_outputs_error_for_missing_query(self) -> None:
        with (
            patch("sys.argv", ["hermes_mem0_tool.py"]),
            patch("sys.stdin", io.StringIO("")),
            contextlib.redirect_stdout(io.StringIO()) as stdout,
        ):
            exit_code = main()

        self.assertEqual(exit_code, 2)
        self.assertFalse(json.loads(stdout.getvalue())["ok"])

    def test_main_calls_guarded_read(self) -> None:
        mocked_read = {
            "query": "active collection",
            "mode": "close-margin",
            "strategy": "score_plus_created_at_rank_close_margin",
            "mem0_cache_hit": False,
            "input_count": 1,
            "total_latency_s": 1.0,
            "mem0_search_latency_s": 1.0,
            "rerank_latency_s": 0.0,
            "results": [{"id": "1", "memory": "mem0_nomic_768"}],
        }
        with (
            patch("sys.argv", ["hermes_mem0_tool.py", "--query", "active collection"]),
            patch("scripts.hermes_mem0_tool.run_guarded_read", return_value=mocked_read),
            contextlib.redirect_stdout(io.StringIO()) as stdout,
        ):
            exit_code = main()

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["memories"][0]["memory"], "mem0_nomic_768")


if __name__ == "__main__":
    unittest.main()
