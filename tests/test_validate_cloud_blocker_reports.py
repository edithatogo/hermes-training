from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_cloud_blocker_reports import validate_semantics


class ValidateCloudBlockerReportsTests(unittest.TestCase):
    def test_empty_matrix_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            matrix = tmpdir / "matrix.json"
            checklist = tmpdir / "checklist.json"
            matrix.write_text(json.dumps({"rows": []}))
            checklist.write_text(json.dumps({"items": []}))

            failures: list[str] = []
            validate_semantics(matrix, checklist, failures)

        self.assertTrue(any("has no blocked track rows" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
