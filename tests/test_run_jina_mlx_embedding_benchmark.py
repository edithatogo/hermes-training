from __future__ import annotations

import unittest

from scripts.run_jina_mlx_embedding_benchmark import render_summary_markdown


class JinaMlxEmbeddingBenchmarkTests(unittest.TestCase):
    def test_summary_markdown_includes_mean_latency(self) -> None:
        summary = {
            "run_id": "jina-smoke",
            "created_at": "2026-06-12T00:00:00+00:00",
            "model": "jinaai/jina-embeddings-v5-omni-small-mlx",
            "task_type": "retrieval",
            "repo_dir": "/tmp/jina",
            "cases": 1,
            "top1_accuracy": 1.0,
            "recall_at_3": 1.0,
            "mrr": 1.0,
            "ndcg_at_3": 1.0,
            "embedding_dims": 1024,
            "embed_latency_mean_s": 0.03,
            "embed_latency_p50_s": 0.02,
            "embed_latency_p95_s": 0.05,
        }
        rows = [{"id": "case-1", "top_doc_id": "doc-1", "top1_pass": True}]

        markdown = render_summary_markdown(summary, rows)

        self.assertIn("Embed latency mean", markdown)
        self.assertIn("0.030s", markdown)


if __name__ == "__main__":
    unittest.main()
