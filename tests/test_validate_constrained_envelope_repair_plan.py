from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_constrained_envelope_repair_plan import validate_plan


class ValidateConstrainedEnvelopeRepairPlanTests(unittest.TestCase):
    def test_validator_rejects_missing_strict_scoring_and_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = root / "plan.json"
            md = root / "plan.md"
            md.write_text("# Plan\n", encoding="utf-8")
            plan.write_text(
                json.dumps(
                    {
                        "promotion_allowed": False,
                        "candidates": [
                            {
                                "candidate": "Nanbeige/Nanbeige4.1-3B",
                                "priority": "high",
                                "case_metrics": {"matched_tool_calls_extra_text": 2},
                                "promotion_boundary": "No promotion from this plan.",
                                "diagnostic_command": "python script.py",
                                "variants": [
                                    {
                                        "result_report": "missing.md",
                                        "source": {
                                            "summary": str(root / "missing-summary.json"),
                                            "results": str(root / "missing-results.jsonl"),
                                            "responses": str(root / "missing-responses.jsonl"),
                                        },
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            failures = validate_plan(plan, md)

        self.assertTrue(any("strict no-extra-text" in failure for failure in failures))
        self.assertTrue(any("missing source results" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
