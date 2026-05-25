from __future__ import annotations

import unittest
from unittest.mock import patch

from scripts.mem0_rerank_search import qwen3_server_rerank, rerank_search_results


class Mem0RerankSearchTests(unittest.TestCase):
    def test_empty_results_do_not_load_qwen_model(self) -> None:
        with patch("scripts.mem0_rerank_search.qwen3_causal_lm_rerank") as mocked:
            ranked, latency = rerank_search_results(
                "missing memory",
                [],
                "qwen3_causal_lm",
                0.20,
                "Qwen/Qwen3-Reranker-0.6B",
                "auto",
                4096,
                "Retrieve relevant memory",
            )

        self.assertEqual(ranked, [])
        self.assertEqual(latency, 0.0)
        mocked.assert_not_called()

    def test_qwen3_strategy_requires_model(self) -> None:
        with self.assertRaisesRegex(ValueError, "--model is required"):
            rerank_search_results(
                "active mem0 collection",
                [{"memory": "The active collection is mem0_nomic_768.", "score": 0.9}],
                "qwen3_causal_lm",
                0.20,
                None,
                "auto",
                4096,
                "Retrieve relevant memory",
            )

    def test_mlx_cross_encoder_strategy_requires_model(self) -> None:
        with self.assertRaisesRegex(ValueError, "--model is required"):
            rerank_search_results(
                "active mem0 collection",
                [{"memory": "The active collection is mem0_nomic_768.", "score": 0.9}],
                "mlx_cross_encoder",
                0.20,
                None,
                "auto",
                4096,
                "Retrieve relevant memory",
            )

    def test_qwen3_strategy_delegates_to_causal_lm_reranker(self) -> None:
        results = [
            {"memory": "Old collection was mem0_old.", "score": 0.91},
            {"memory": "Current collection is mem0_nomic_768.", "score": 0.88},
        ]
        expected = [dict(results[1], rerank_score=0.99), dict(results[0], rerank_score=0.1)]

        with patch("scripts.mem0_rerank_search.qwen3_causal_lm_rerank", return_value=(expected, 0.123)) as mocked:
            ranked, latency = rerank_search_results(
                "What is the active mem0 collection?",
                results,
                "qwen3_causal_lm",
                0.20,
                "Qwen/Qwen3-Reranker-0.6B",
                "cpu",
                4096,
                "Retrieve relevant memory",
                True,
            )

        self.assertEqual(ranked, expected)
        self.assertEqual(latency, 0.123)
        mocked.assert_called_once_with(
            "Qwen/Qwen3-Reranker-0.6B",
            "What is the active mem0 collection?",
            results,
            "cpu",
            4096,
            "Retrieve relevant memory",
            local_files_only=True,
        )

    def test_qwen3_strategy_uses_warm_server_when_configured(self) -> None:
        results = [{"memory": "Current collection is mem0_nomic_768.", "score": 0.88}]
        expected = [dict(results[0], rerank_score=0.99)]

        with (
            patch("scripts.mem0_rerank_search.qwen3_server_rerank", return_value=(expected, 0.02)) as server,
            patch("scripts.mem0_rerank_search.qwen3_causal_lm_rerank") as local,
        ):
            ranked, latency = rerank_search_results(
                "What is the active mem0 collection?",
                results,
                "qwen3_causal_lm",
                0.20,
                "Qwen/Qwen3-Reranker-0.6B",
                "cpu",
                4096,
                "Retrieve relevant memory",
                False,
                "http://127.0.0.1:8765",
            )

        self.assertEqual(ranked, expected)
        self.assertEqual(latency, 0.02)
        local.assert_not_called()
        server.assert_called_once()

    def test_mlx_cross_encoder_strategy_delegates_to_mlx_backend(self) -> None:
        results = [
            {"memory": "Old collection was mem0_old.", "score": 0.91},
            {"memory": "Current collection is mem0_nomic_768.", "score": 0.88},
        ]
        expected = [dict(results[1], rerank_score=0.99), dict(results[0], rerank_score=0.1)]

        with patch("scripts.mem0_rerank_search.mlx_cross_encoder_rerank", return_value=(expected, 0.456)) as mocked:
            ranked, latency = rerank_search_results(
                "What is the active mem0 collection?",
                results,
                "mlx_cross_encoder",
                0.20,
                "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
                "cpu",
                4096,
                "Retrieve relevant memory",
                mlx_max_length=1024,
            )

        self.assertEqual(ranked, expected)
        self.assertEqual(latency, 0.456)
        mocked.assert_called_once_with(
            "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit",
            "What is the active mem0 collection?",
            results,
            1024,
        )

    def test_qwen3_server_rerank_posts_json(self) -> None:
        class FakeResponse:
            def __enter__(self) -> "FakeResponse":
                return self

            def __exit__(self, *_: object) -> None:
                return None

            def read(self) -> bytes:
                return b'{"rerank_latency_s": 0.02, "results": [{"id": "new"}]}'

        with patch("scripts.mem0_rerank_search.urlopen", return_value=FakeResponse()) as opened:
            ranked, latency = qwen3_server_rerank(
                "http://127.0.0.1:8765/",
                "query",
                [{"id": "new", "memory": "answer"}],
                "Qwen/Qwen3-Reranker-0.6B",
                "cpu",
                4096,
                "Retrieve relevant memory",
                True,
            )

        request = opened.call_args.args[0]
        payload = request.data.decode("utf-8")
        self.assertEqual(request.full_url, "http://127.0.0.1:8765/rerank")
        self.assertIn('"query": "query"', payload)
        self.assertIn('"local_files_only": true', payload)
        self.assertEqual(ranked, [{"id": "new"}])
        self.assertEqual(latency, 0.02)


if __name__ == "__main__":
    unittest.main()
