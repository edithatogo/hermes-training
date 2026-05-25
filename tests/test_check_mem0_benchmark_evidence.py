from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_mem0_benchmark_evidence import build_report, validate_file


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data) + "\n", encoding="utf-8")


BASE = {
    "run_id": "run",
    "created_at": "2026-05-26T00:00:00+00:00",
    "suite": "suite.json",
    "output_dir": "/Volumes/PortableSSD/hermes-evals/out",
}


class Mem0BenchmarkEvidenceTests(unittest.TestCase):
    def test_embedding_summary_requires_positive_dims(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "embedding-benchmark" / "run" / "summary.json"
            write_json(
                path,
                {
                    **BASE,
                    "model": "nomic-embed-text:latest",
                    "cases": 2,
                    "top1_accuracy": 1.0,
                    "recall_at_3": 1.0,
                    "mrr": 1.0,
                    "ndcg_at_3": 1.0,
                    "embedding_dims": 0,
                    "embed_latency_mean_s": 0.1,
                    "embed_latency_p50_s": 0.1,
                    "embed_latency_p95_s": 0.1,
                },
            )

            item = validate_file("embedding", path, root)

            self.assertEqual(item["status"], "failed")
            self.assertIn("embedding_dims must be a positive integer", item["errors"])

    def test_blocked_reranking_accepts_zero_case_timebox_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "mem0-reranking-benchmark" / "blocked" / "summary.json"
            write_json(
                path,
                {
                    **BASE,
                    "status": "blocked",
                    "model": "onnx-community/Qwen3-Reranker-0.6B-ONNX",
                    "blocker": "timed out",
                    "elapsed_s": 180.0,
                    "runtime": "transformers.js",
                    "npm_package": "@huggingface/transformers@4.2.0",
                    "device": "cpu",
                    "dtype": "q4",
                    "max_length": 512,
                    "limit_cases": 1,
                    "tool_root": "/Volumes/PortableSSD/hermes-tools/transformersjs-qwen3-reranker",
                    "cache_root": "/Volumes/PortableSSD/huggingface/transformers",
                    "cases": 0,
                },
            )

            self.assertEqual(validate_file("reranking", path, root)["status"], "passed")

    def test_report_fails_when_required_kind_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "embedding-benchmark" / "run" / "summary.json"
            write_json(
                path,
                {
                    **BASE,
                    "model": "nomic-embed-text:latest",
                    "cases": 2,
                    "top1_accuracy": 1.0,
                    "recall_at_3": 1.0,
                    "mrr": 1.0,
                    "ndcg_at_3": 1.0,
                    "embedding_dims": 768,
                    "embed_latency_mean_s": 0.1,
                    "embed_latency_p50_s": 0.1,
                    "embed_latency_p95_s": 0.1,
                },
            )

            report = build_report(root)

            self.assertEqual(report["status"], "failed")
            self.assertIn("memory", report["missing_kinds"])


if __name__ == "__main__":
    unittest.main()
