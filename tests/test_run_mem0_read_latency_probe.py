from __future__ import annotations

import argparse
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.run_mem0_read_latency_probe import (
    build_read_args,
    build_mem0_read_command,
    load_queries,
    main,
    read_wall_timeout,
    run_guarded_read_subprocess,
    summarize,
)


class RunMem0ReadLatencyProbeTests(unittest.TestCase):
    def test_load_queries_accepts_strings_and_objects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "queries.json"
            path.write_text(json.dumps(["one", {"query": "two"}]), encoding="utf-8")

            self.assertEqual(load_queries(path, []), ["one", "two"])

    def test_inline_queries_override_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "queries.json"
            path.write_text(json.dumps(["file"]), encoding="utf-8")

            self.assertEqual(load_queries(path, ["inline"]), ["inline"])

    def test_summarize_counts_singleton_multi_and_empty(self) -> None:
        args = argparse.Namespace(tool="cmd", mode="close-margin", iterations=1, model="")
        rows = [
            {
                "query": "a",
                "strategy": "score_plus_created_at_rank_close_margin",
                "input_count": 1,
                "total_latency_s": 2.0,
                "mem0_search_latency_s": 2.0,
                "rerank_latency_s": 0.0,
                "fallback_reason": "",
                "mem0_cache_hit": False,
            },
            {
                "query": "b",
                "strategy": "score_plus_created_at_rank_close_margin",
                "input_count": 3,
                "total_latency_s": 4.0,
                "mem0_search_latency_s": 3.9,
                "rerank_latency_s": 0.1,
                "fallback_reason": "fallback",
                "mem0_cache_hit": True,
            },
            {
                "query": "c",
                "strategy": "score_plus_created_at_rank_close_margin",
                "input_count": 0,
                "total_latency_s": 1.0,
                "mem0_search_latency_s": 1.0,
                "rerank_latency_s": 0.0,
                "fallback_reason": "",
                "mem0_cache_hit": False,
            },
        ]

        summary = summarize(rows, "run", Path("/tmp/out"), ["a", "b", "c"], args)

        self.assertEqual(summary["case_count"], 3)
        self.assertEqual(summary["singleton_count"], 1)
        self.assertEqual(summary["multi_result_count"], 1)
        self.assertEqual(summary["empty_count"], 1)
        self.assertEqual(summary["fallback_count"], 1)
        self.assertEqual(summary["mem0_cache_hit_count"], 1)
        self.assertEqual(summary["total_latency_p50_s"], 2.0)
        self.assertEqual(summary["scenario_summaries"]["cold"]["count"], 2)
        self.assertEqual(summary["scenario_summaries"]["cache_hit"]["count"], 1)

    def test_summarize_uses_actual_read_model_for_mlx_bge(self) -> None:
        args = argparse.Namespace(tool="cmd", mode="mlx-bge", iterations=1, model="Qwen/Qwen3-Reranker-0.6B")
        rows = [
            {
                "query": "a",
                "strategy": "mlx_cross_encoder",
                "model": "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
                "input_count": 1,
                "total_latency_s": 13.0,
                "mem0_search_latency_s": 0.0,
                "rerank_latency_s": 0.058,
                "fallback_reason": "",
                "mem0_cache_hit": True,
            }
        ]

        summary = summarize(rows, "run", Path("/tmp/out"), ["a"], args)

        self.assertEqual(summary["model"], "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit")

    def test_build_read_args_preserves_guarded_options(self) -> None:
        args = argparse.Namespace(
            tool="cmd",
            mode="qwen3",
            timeout_s=12.0,
            recency_weight=0.2,
            model="Qwen/Qwen3-Reranker-0.6B",
            qwen3_device="auto",
            qwen3_max_length=4096,
            mlx_max_length=1024,
            qwen3_instruction="Retrieve",
            qwen3_local_files_only=True,
            qwen3_server_url="http://127.0.0.1:8765",
            fallback_to_vector=True,
            include_raw=False,
            cache_path=Path("/tmp/cache.json"),
            cache_ttl_s=60.0,
            refresh_cache=True,
        )

        read_args = build_read_args(args, "query")

        self.assertEqual(read_args.query, "query")
        self.assertEqual(read_args.mode, "qwen3")
        self.assertTrue(read_args.fallback_to_vector)
        self.assertEqual(read_args.qwen3_server_url, "http://127.0.0.1:8765")
        self.assertEqual(read_args.cache_path, Path("/tmp/cache.json"))
        self.assertEqual(read_args.cache_ttl_s, 60.0)
        self.assertTrue(read_args.refresh_cache)
        self.assertEqual(read_args.mlx_max_length, 1024)

    def test_build_read_args_preserves_mlx_bge_options(self) -> None:
        args = argparse.Namespace(
            tool="cmd",
            mode="mlx-bge",
            timeout_s=180.0,
            recency_weight=0.2,
            model="flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
            qwen3_device="auto",
            qwen3_max_length=4096,
            mlx_max_length=2048,
            qwen3_instruction="Retrieve",
            qwen3_local_files_only=False,
            qwen3_server_url=None,
            fallback_to_vector=True,
            include_raw=False,
            cache_path=None,
            cache_ttl_s=300.0,
            refresh_cache=False,
        )

        read_args = build_read_args(args, "active collection")

        self.assertEqual(read_args.mode, "mlx-bge")
        self.assertEqual(read_args.model, "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit")
        self.assertEqual(read_args.mlx_max_length, 2048)
        self.assertTrue(read_args.fallback_to_vector)

    def test_main_writes_summary_with_mocked_reads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "out"
            argv = [
                "run_mem0_read_latency_probe.py",
                "--query",
                "active collection",
                "--output-dir",
                str(output_dir),
                "--run-id",
                "mock-run",
            ]
            mocked_output = {
                "query": "active collection",
                "strategy": "score_plus_created_at_rank_close_margin",
                "input_count": 1,
                "total_latency_s": 2.0,
                "mem0_search_latency_s": 2.0,
                "rerank_latency_s": 0.0,
                "fallback_reason": "",
                "mem0_cache_hit": False,
            }
            with (
                patch("sys.argv", argv),
                patch("scripts.run_mem0_read_latency_probe.run_guarded_read", return_value=mocked_output),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(main(), 0)

            summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

        self.assertEqual(summary["run_id"], "mock-run")
        self.assertEqual(summary["case_count"], 1)
        self.assertEqual(summary["singleton_count"], 1)

    def test_read_wall_timeout_noops_when_disabled(self) -> None:
        with read_wall_timeout(0):
            value = "ok"

        self.assertEqual(value, "ok")

    def test_subprocess_command_includes_mlx_bge_options(self) -> None:
        args = argparse.Namespace(
            tool="cmd",
            mode="mlx-bge",
            timeout_s=180.0,
            recency_weight=0.2,
            model="flaglow/model",
            qwen3_device="auto",
            qwen3_max_length=4096,
            mlx_max_length=2048,
            qwen3_instruction="Retrieve",
            qwen3_local_files_only=False,
            qwen3_server_url=None,
            fallback_to_vector=True,
            include_raw=False,
            cache_path=None,
            cache_ttl_s=300.0,
            refresh_cache=False,
        )

        command = build_mem0_read_command(args, "query")

        self.assertIn("--mode", command)
        self.assertIn("mlx-bge", command)
        self.assertIn("--mlx-max-length", command)
        self.assertIn("2048", command)
        self.assertIn("--fallback-to-vector", command)

    def test_subprocess_read_parses_json(self) -> None:
        args = argparse.Namespace(
            tool="cmd",
            mode="close-margin",
            timeout_s=120.0,
            recency_weight=0.2,
            model="Qwen/Qwen3-Reranker-0.6B",
            qwen3_device="auto",
            qwen3_max_length=4096,
            mlx_max_length=1024,
            qwen3_instruction="Retrieve",
            qwen3_local_files_only=False,
            qwen3_server_url=None,
            fallback_to_vector=False,
            include_raw=False,
            cache_path=None,
            cache_ttl_s=0.0,
            refresh_cache=False,
            read_wall_timeout_s=10.0,
        )
        completed = argparse.Namespace(stdout='{"query":"q","total_latency_s":1.0}', stderr="")
        with patch("scripts.run_mem0_read_latency_probe.subprocess.run", return_value=completed):
            output = run_guarded_read_subprocess(args, "q")

        self.assertEqual(output["query"], "q")


if __name__ == "__main__":
    unittest.main()
