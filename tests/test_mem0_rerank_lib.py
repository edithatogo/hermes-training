from __future__ import annotations

import unittest

from scripts.mem0_rerank_lib import parse_mem0_search_output, rerank_results


class Mem0RerankLibTest(unittest.TestCase):
    def test_created_at_rank_can_promote_newer_conflicting_memory(self) -> None:
        results = [
            {
                "id": "old",
                "memory": "The active mem0 Qdrant collection is mem0_legacy_1024.",
                "score": 0.917,
                "created_at": "2026-05-24T06:53:45+00:00",
            },
            {
                "id": "new",
                "memory": "The active mem0 Qdrant collection is mem0_nomic_768 with 768 dimensions.",
                "score": 0.880,
                "created_at": "2026-05-24T06:53:48+00:00",
            },
        ]

        ranked = rerank_results(results, "score_plus_created_at_rank", 0.20)

        self.assertEqual(ranked[0]["id"], "new")
        self.assertGreater(ranked[0]["rerank_score"], ranked[1]["rerank_score"])

    def test_created_at_rank_does_not_beat_large_semantic_margin(self) -> None:
        results = [
            {
                "id": "relevant_old",
                "memory": "Large GGUF exports should stay under /Volumes/PortableSSD/hermes-exports.",
                "score": 0.90,
                "created_at": "2026-05-24T06:53:24+00:00",
            },
            {
                "id": "irrelevant_new",
                "memory": "Short benchmark report markdown files can be committed to the git repository.",
                "score": 0.50,
                "created_at": "2026-05-24T06:53:27+00:00",
            },
        ]

        ranked = rerank_results(results, "score_plus_created_at_rank", 0.20)

        self.assertEqual(ranked[0]["id"], "relevant_old")

    def test_parse_mem0_search_output_ignores_warning_prefix(self) -> None:
        raw = """Failed to load spaCy lemma model: spaCy is not installed.
{
  "results": [
    {
      "id": "abc",
      "memory": "The active mem0 collection is mem0_nomic_768.",
      "score": 0.72,
      "created_at": "2026-05-24T06:53:48+00:00"
    }
  ]
}
Exception ignored while calling deallocator
"""

        results = parse_mem0_search_output(raw)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "abc")


if __name__ == "__main__":
    unittest.main()
