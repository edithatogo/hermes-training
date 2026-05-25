from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_publication_dataset_sources import summarize


class PublicationDatasetSourceAuditTests(unittest.TestCase):
    def test_summarize_groups_missing_source_as_seed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            row = {
                "id": "seed-1",
                "messages": [{"role": "user", "content": "Hello"}],
            }
            (root / "train.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")

            summary = summarize(root)

            self.assertEqual(summary["source_counts"]["strict_tool_call_seed"], 1)
            self.assertEqual(summary["review_result"], "reviewed_with_caveats")

    def test_unknown_source_blocks_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            row = {
                "id": "external-1",
                "source": "external_unknown",
                "messages": [{"role": "user", "content": "Hello"}],
            }
            (root / "train.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")

            summary = summarize(root)

            self.assertEqual(summary["review_result"], "blocked")
            self.assertEqual(summary["unknown_sources"], ["external_unknown"])


if __name__ == "__main__":
    unittest.main()
