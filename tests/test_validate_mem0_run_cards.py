from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_mem0_run_cards import parse_index_rows, validate_run_card


class ValidateMem0RunCardsTests(unittest.TestCase):
    def test_parse_index_rows_reads_output_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            index = Path(tmp) / "index.md"
            index.write_text(
                "# index\n\n"
                "| Kind | Run ID | Model/Tool | Raw Pass | Rerank Pass | Top-1 | Recall@k/3 | JSON Valid | Latency p50 | Output |\n"
                "|---|---|---|---:|---:|---:|---:|---:|---:|---|\n"
                "| embedding | run-a | model | 1.000 |  | 1.000 | 1.000 |  | 0.010 | `/tmp/run-a` |\n",
                encoding="utf-8",
            )

            rows = parse_index_rows(index)

        self.assertEqual(rows, [{"kind": "embedding", "run_id": "run-a", "output": "/tmp/run-a"}])

    def test_validate_run_card_requires_existing_summary_and_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            output = tmpdir / "run-a"
            output.mkdir()
            summary = output / "summary.json"
            summary.write_text("{}", encoding="utf-8")
            card = tmpdir / "run-a.md"
            card.write_text(
                "# mem0 Run Card\n\n"
                "Run ID: run-a\n"
                f"Summary: `{summary}`\n\n"
                "## Candidate\n\n## Command\n\n## Result\n\n## Decision\n",
                encoding="utf-8",
            )

            failures = validate_run_card(card, {"run_id": "run-a", "output": str(output)})

        self.assertEqual(failures, [])

    def test_validate_run_card_reports_missing_card(self) -> None:
        failures = validate_run_card(Path("/tmp/does-not-exist-card.md"), {"run_id": "missing", "output": ""})

        self.assertTrue(any("missing run card" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
