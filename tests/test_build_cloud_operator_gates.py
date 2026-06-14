from __future__ import annotations

import unittest

from scripts.build_cloud_operator_gates import build_report, gate_rows
from scripts.validate_cloud_operator_gates import validate_semantics


class BuildCloudOperatorGatesTests(unittest.TestCase):
    def test_gate_rows_keep_execution_fail_closed(self) -> None:
        rows = gate_rows(
            {
                "items": [
                    {
                        "backend": "modal",
                        "status": "prepared-needs-credit-and-gpu-policy-check",
                        "blocker": "needs policy",
                        "commands": ["./.venv/bin/python scripts/validate_modal_policy_gate.py"],
                    }
                ]
            }
        )

        self.assertEqual(rows[0]["backend"], "modal")
        self.assertFalse(rows[0]["execution_allowed"])
        self.assertFalse(rows[0]["promotion_allowed"])
        self.assertTrue(any("modal-policy-evidence" in item for item in rows[0]["external_evidence_required"]))

    def test_validator_requires_all_cloud_backends(self) -> None:
        report = {
            "execution_allowed": False,
            "promotion_allowed": False,
            "rows": [
                {
                    "backend": "modal",
                    "execution_allowed": False,
                    "promotion_allowed": False,
                    "external_evidence_required": ["evidence"],
                    "secret_policy": "Do not commit token secret payment card data.",
                }
            ],
        }

        failures = validate_semantics(report)

        self.assertTrue(any("missing backend gates" in failure for failure in failures))

    def test_full_report_passes_semantic_validation(self) -> None:
        report = {
            "execution_allowed": False,
            "promotion_allowed": False,
            "rows": [
                {
                    "backend": backend,
                    "execution_allowed": False,
                    "promotion_allowed": False,
                    "external_evidence_required": ["evidence"],
                    "secret_policy": "Do not commit token secret payment card data.",
                }
                for backend in ("colab", "hf_jobs", "azure", "ngc", "kaggle", "modal", "lightning")
            ],
        }

        self.assertEqual(validate_semantics(report), [])


if __name__ == "__main__":
    unittest.main()
