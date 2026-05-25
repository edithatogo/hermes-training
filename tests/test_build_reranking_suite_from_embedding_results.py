import unittest

from scripts.build_reranking_suite_from_embedding_results import build_suite


class BuildRerankingSuiteFromEmbeddingResultsTest(unittest.TestCase):
    def test_preserves_scores_text_and_timestamps(self) -> None:
        embedding_suite = [
            {
                "id": "case-1",
                "category": "recency_conflict",
                "query": "current preference?",
                "documents": [
                    {
                        "id": "old",
                        "text": "The old preference was A.",
                        "created_at": "2026-05-24T05:00:00+00:00",
                        "relevant": False,
                    },
                    {
                        "id": "new",
                        "text": "The current preference is B.",
                        "created_at": "2026-05-24T07:00:00+00:00",
                        "relevant": True,
                    },
                ],
            }
        ]
        result_rows = [
            {
                "id": "case-1",
                "ranked_docs": [
                    {"id": "old", "score": 0.74},
                    {"id": "new", "score": 0.73},
                ],
            }
        ]

        built = build_suite(embedding_suite, result_rows)

        self.assertEqual(built[0]["category"], "recency_conflict")
        self.assertEqual(built[0]["candidates"][0]["text"], "The old preference was A.")
        self.assertEqual(built[0]["candidates"][0]["score"], 0.74)
        self.assertEqual(built[0]["candidates"][1]["created_at"], "2026-05-24T07:00:00+00:00")
        self.assertTrue(built[0]["candidates"][1]["relevant"])

