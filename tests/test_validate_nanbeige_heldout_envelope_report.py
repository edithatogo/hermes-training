from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_nanbeige_heldout_envelope_report import validate_report


class ValidateNanbeigeHeldoutEnvelopeReportTests(unittest.TestCase):
    def test_rejects_promotional_or_full_pass_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = root / "report.json"
            markdown = root / "report.md"
            markdown.write_text("# report\n", encoding="utf-8")
            report.write_text(
                json.dumps(
                    {
                        "model": "Nanbeige/Nanbeige4.1-3B",
                        "suite": "benchmarks/tool_call_local/heldout_suite.json",
                        "promotion_allowed": True,
                        "cases": 8,
                        "raw_pass_rate": 0.125,
                        "constrained_pass_rate": 1.0,
                        "claim_boundary": "promotion",
                        "source_output_dir": str(root / "missing-source"),
                        "source_summary": str(root / "missing-summary.json"),
                        "output_dir": str(root / "missing-output"),
                        "case_results": [],
                    }
                ),
                encoding="utf-8",
            )

            failures = validate_report(report, markdown)

        self.assertTrue(any("promotion_allowed false" in failure for failure in failures))
        self.assertTrue(any("must not be represented as a pass" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
