from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_scorecard_backend_selection import validate_semantics


class ValidateScorecardBackendSelectionTests(unittest.TestCase):
    def test_rejects_execution_enabled_selection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "selection.json"
            path.write_text(
                json.dumps(
                    {
                        "status": "ready",
                        "execute": True,
                        "promotion_allowed": True,
                        "selected_backend": "colab",
                        "required_before_execution": [],
                        "ranked_backends": [{"backend": "colab", "score": 100}],
                    }
                ),
                encoding="utf-8",
            )

            failures = validate_semantics(path)

        self.assertTrue(any("must not enable execution" in failure for failure in failures))
        self.assertTrue(any("must not allow benchmark promotion" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
