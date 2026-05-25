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
    load_queries,
    main,
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
            },
            {
                "query": "b",
                "strategy": "score_plus_created_at_rank_close_margin",
                "input_count": 3,
                "total_latency_s": 4.0,
                "mem0_search_latency_s": 3.9,
                "rerank_latency_s": 0.1,
                "fallback_reason": "fallback",
            },
            {
                "query": "c",
                "strategy": "score_plus_created_at_rank_close_margin",
                "input_count": 0,
                "total_latency_s": 1.0,
                "mem0_search_latency_s": 1.0,
                "rerank_latency_s": 0.0,
                "fallback_reason": "",
            },
        ]

        summary = summarize(rows, "run", Path("/tmp/out"), ["a", "b", "c"], args)

        self.assertEqual(summary["case_count"], 3)
        self.assertEqual(summary["singleton_count"], 1)
        self.assertEqual(summary["multi_result_count"], 1)
        self.assertEqual(summary["empty_count"], 1)
        self.assertEqual(summary["fallback_count"], 1)
        self.assertEqual(summary["total_latency_p50_s"], 2.0)

    def test_build_read_args_preserves_guarded_options(self) -> None:
        args = argparse.Namespace(
            tool="cmd",
            mode="qwen3",
            timeout_s=12.0,
            recency_weight=0.2,
            model="Qwen/Qwen3-Reranker-0.6B",
            qwen3_device="auto",
            qwen3_max_length=4096,
            qwen3_instruction="Retrieve",
            qwen3_local_files_only=True,
            qwen3_server_url="http://127.0.0.1:8765",
            fallback_to_vector=True,
            include_raw=False,
        )

        read_args = build_read_args(args, "query")

        self.assertEqual(read_args.query, "query")
        self.assertEqual(read_args.mode, "qwen3")
        self.assertTrue(read_args.fallback_to_vector)
        self.assertEqual(read_args.qwen3_server_url, "http://127.0.0.1:8765")

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


if __name__ == "__main__":
    unittest.main()
