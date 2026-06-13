from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.render_mem0_embeddinggemma_config import render_config


class RenderMem0EmbeddingGemmaConfigTests(unittest.TestCase):
    def test_render_keeps_llm_and_switches_embedding_profile(self) -> None:
        base = {
            "user_id": "example-user",
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "mem0_nomic_768",
                    "embedding_model_dims": 768,
                    "path": "/Users/example/.mem0/qdrant",
                    "on_disk": True,
                },
            },
            "llm": {"provider": "ollama", "config": {"model": "sam860/LFM2:2.6b"}},
            "embedder": {
                "provider": "ollama",
                "config": {"model": "nomic-embed-text:latest", "embedding_dims": 768},
            },
            "history_db_path": "/Users/example/.mem0/history.db",
            "version": "v1.1",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = render_config(
                base,
                collection_name="mem0_embeddinggemma_300m_768",
                qdrant_path=root / "qdrant",
                history_db_path=root / "history.db",
                base_url="http://127.0.0.1:8105/v1/",
                model="embeddinggemma-300m-qat-Q4_0.gguf",
                dims=768,
                api_key="local-profile",
            )
        self.assertEqual(config["llm"], base["llm"])
        self.assertEqual(config["vector_store"]["config"]["collection_name"], "mem0_embeddinggemma_300m_768")
        self.assertEqual(config["vector_store"]["config"]["embedding_model_dims"], 768)
        self.assertEqual(config["embedder"]["provider"], "openai")
        self.assertEqual(config["embedder"]["config"]["openai_base_url"], "http://127.0.0.1:8105/v1")
        self.assertEqual(config["embedder"]["config"]["model"], "embeddinggemma-300m-qat-Q4_0.gguf")


if __name__ == "__main__":
    unittest.main()
