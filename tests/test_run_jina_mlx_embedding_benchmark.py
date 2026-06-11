from __future__ import annotations

import unittest
import sys
import tempfile
from pathlib import Path
from unittest import mock

from scripts.run_jina_mlx_embedding_benchmark import load_model, render_summary_markdown


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

    def test_load_model_falls_back_to_model_py_when_utils_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_dir = Path(temp_dir)
            (repo_dir / "config.json").write_text('{"hidden_size": 4}\n', encoding="utf-8")
            (repo_dir / "model.py").write_text(
                "\n".join(
                    [
                        "class OmniSmallConfig:",
                        "    @classmethod",
                        "    def from_dict(cls, data):",
                        "        inst = cls()",
                        "        inst.data = data",
                        "        return inst",
                        "",
                        "class JinaOmniSmallEmbeddingModel:",
                        "    def __init__(self, config):",
                        "        self.config = config",
                        "        self.loaded = []",
                        "    def sanitize(self, weights):",
                        "        return weights",
                        "    def load_weights(self, weights):",
                        "        self.loaded = weights",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            sys.modules.pop("model", None)
            with mock.patch("scripts.run_jina_mlx_embedding_benchmark.mx.load", return_value={"w": 1}):
                model = load_model(repo_dir)

            self.assertEqual(model.config.data["hidden_size"], 4)
            self.assertEqual(model.loaded, [("w", 1)])


if __name__ == "__main__":
    unittest.main()
