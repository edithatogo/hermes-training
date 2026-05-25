import unittest
from pathlib import Path

from scripts.run_sentence_transformers_embedding_benchmark import load_json, validate_suite


class EmbeddingBenchmarkSuitesTest(unittest.TestCase):
    def test_expanded_memory_retrieval_suite_is_valid(self) -> None:
        suite_path = Path("benchmarks/embeddings/memory_retrieval_expanded_suite.json")
        suite = load_json(suite_path)

        validate_suite(suite, suite_path)

        self.assertGreaterEqual(len(suite), 10)
        categories = {case.get("category") for case in suite}
        self.assertIn("direct_recall", categories)
        self.assertIn("recency_conflict", categories)
        self.assertIn("distractor_resistance", categories)

