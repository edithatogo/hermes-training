from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.validate_prompt_profile_repair_results import validate_results


class ValidatePromptProfileRepairResultsTests(unittest.TestCase):
    def test_validate_results_requires_existing_report_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            results = root / "results.json"
            results.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "candidate": "model",
                                "variant": "variant",
                                "status": "completed-no-promotion",
                                "pass_rate": 0.0,
                                "cases": 3,
                                "passed": 0,
                                "promotion_allowed": False,
                                "result_report": "missing.md",
                                "source_summary": str(root / "missing-summary.json"),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            failures = validate_results(results)

        self.assertTrue(any("missing result report" in failure for failure in failures))
        self.assertTrue(any("missing source summary" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
