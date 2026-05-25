from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.run_mem0_isolated_fixture_rerank import (
    annotate_relevance,
    preferred_summary_metrics,
    safe_collection_suffix,
    score_ranking,
    write_fixture_config,
)


class RunMem0IsolatedFixtureRerankTests(unittest.TestCase):
    def test_write_fixture_config_uses_output_local_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = root / "base.json"
            base.write_text(
                json.dumps(
                    {
                        "vector_store": {
                            "provider": "qdrant",
                            "config": {
                                "collection_name": "mem0_nomic_768",
                                "embedding_model_dims": 768,
                                "path": "/Users/doughnut/.mem0/qdrant",
                            },
                        },
                        "history_db_path": "/Users/doughnut/.mem0/history.db",
                    }
                ),
                encoding="utf-8",
            )

            config_path = write_fixture_config(base, root / "out", "Fixture Run 2026")
            config = json.loads(config_path.read_text(encoding="utf-8"))

        self.assertEqual(config["vector_store"]["config"]["collection_name"], "mem0_fixture_fixture_run_2026")
        self.assertTrue(config["vector_store"]["config"]["path"].endswith("/out/qdrant"))
        self.assertTrue(config["history_db_path"].endswith("/out/history.db"))

    def test_annotate_relevance_marks_expected_fragments(self) -> None:
        case = {"expected": {"must_retrieve_any": ["nomic-embed-text"]}}
        results = [
            {"memory": "The current embedder is nomic-embed-text."},
            {"memory": "BGE-M3 is a candidate."},
        ]

        annotated = annotate_relevance(case, results)

        self.assertTrue(annotated[0]["relevant"])
        self.assertFalse(annotated[1]["relevant"])

    def test_score_ranking_uses_top3_relevance(self) -> None:
        case = {
            "expected": {
                "must_retrieve_any": ["target"],
                "top_result_should_contain": "target",
            }
        }
        ranked = [
            {"id": "wrong", "memory": "wrong", "relevant": False},
            {"id": "right", "memory": "target", "relevant": True},
        ]

        scored = score_ranking(case, ranked, 0.01)

        self.assertFalse(scored["top1_pass"])
        self.assertEqual(scored["recall_at_3"], 1.0)
        self.assertEqual(scored["reciprocal_rank"], 0.5)

    def test_preferred_summary_metrics_prefers_qwen3_on_tie(self) -> None:
        summary = {
            "strategies": {
                "score_plus_created_at_rank_close_margin": {
                    "top1_accuracy": 1.0,
                    "pass_rate": 1.0,
                    "mrr": 1.0,
                },
                "qwen3_causal_lm:Qwen/Qwen3-Reranker-0.6B": {
                    "top1_accuracy": 1.0,
                    "pass_rate": 1.0,
                    "mrr": 1.0,
                },
            }
        }

        preferred = preferred_summary_metrics(summary)

        self.assertEqual(preferred["strategy"], "qwen3_causal_lm:Qwen/Qwen3-Reranker-0.6B")
        self.assertEqual(preferred["top1_accuracy"], 1.0)

    def test_preferred_summary_metrics_prefers_best_measured_strategy(self) -> None:
        summary = {
            "strategies": {
                "score_plus_created_at_rank_close_margin": {
                    "top1_accuracy": 1.0,
                    "pass_rate": 1.0,
                    "mrr": 1.0,
                },
                "qwen3_causal_lm:Qwen/Qwen3-Reranker-0.6B": {
                    "top1_accuracy": 0.666,
                    "pass_rate": 0.666,
                    "mrr": 0.833,
                },
            }
        }

        preferred = preferred_summary_metrics(summary)

        self.assertEqual(preferred["strategy"], "score_plus_created_at_rank_close_margin")
        self.assertEqual(preferred["top1_accuracy"], 1.0)

    def test_preferred_summary_metrics_can_select_mlx_strategy(self) -> None:
        summary = {
            "strategies": {
                "score_plus_created_at_rank_close_margin": {
                    "top1_accuracy": 0.8,
                    "pass_rate": 0.8,
                    "mrr": 0.9,
                },
                "mlx_cross_encoder:flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit": {
                    "top1_accuracy": 1.0,
                    "pass_rate": 1.0,
                    "mrr": 1.0,
                },
            }
        }

        preferred = preferred_summary_metrics(summary)

        self.assertEqual(
            preferred["strategy"],
            "mlx_cross_encoder:flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
        )

    def test_safe_collection_suffix_removes_punctuation(self) -> None:
        self.assertEqual(safe_collection_suffix("Run 2026-05-26!"), "run_2026_05_26")


if __name__ == "__main__":
    unittest.main()
