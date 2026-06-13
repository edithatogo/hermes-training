from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_kaggle_torch_policy_wheel_proof import validate_report


class ValidateKaggleTorchPolicyWheelProofTests(unittest.TestCase):
    def test_rejects_runtime_scoring_claim_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = root / "report.json"
            markdown = root / "report.md"
            markdown.write_text("# proof\n", encoding="utf-8")
            report.write_text(
                json.dumps(
                    {
                        "policy": "p100-cu118",
                        "python_abi": "cp312-cp312",
                        "platform": "linux_x86_64",
                        "index_url": "https://download.pytorch.org/whl/cu118",
                        "claim_boundary": "runtime scoring is proven",
                        "wheels": [],
                    }
                ),
                encoding="utf-8",
            )

            failures = validate_report(report, markdown)

        self.assertTrue(any("non-scoring claim boundary" in failure for failure in failures))
        self.assertTrue(any("missing wheel proof for torch" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
