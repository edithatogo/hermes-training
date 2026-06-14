from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_modal_policy_gate import build_policy_report, validate_policy_report


class ValidateModalPolicyGateTests(unittest.TestCase):
    def test_empty_billing_keeps_modal_execution_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            billing = root / "billing.json"
            preflight = root / "preflight.json"
            dry_run = root / "dry-run.json"
            billing.write_text("[]\n", encoding="utf-8")
            preflight.write_text(
                json.dumps({"backends": {"modal": {"status": "prepared-needs-credit-and-gpu-policy-check"}}}),
                encoding="utf-8",
            )
            dry_run.write_text(
                json.dumps({"status": "dry-run", "execute": False, "confirm_zero_cost_compute": False}),
                encoding="utf-8",
            )

            report = build_policy_report(billing, preflight, dry_run)
            passed, failures = validate_policy_report(report)

        self.assertTrue(passed, failures)
        self.assertEqual(report["status"], "blocked-needs-zero-cost-policy")
        self.assertFalse(report["execution_allowed"])
        self.assertFalse(report["promotion_allowed"])
        self.assertIn("does not prove free GPU credits", report["claim_boundary"])

    def test_validator_rejects_policy_report_that_allows_execution_without_evidence(self) -> None:
        report = {
            "backend": "modal",
            "status": "blocked-needs-zero-cost-policy",
            "zero_cost_policy_confirmed": False,
            "paid_compute_approved": False,
            "execution_allowed": True,
            "promotion_allowed": False,
            "claim_boundary": "An empty Modal billing report proves no current-month usage rows only.",
            "checks": [{"name": "billing_report_present", "passed": True, "detail": "ok"}],
        }

        passed, failures = validate_policy_report(report)

        self.assertFalse(passed)
        self.assertTrue(any("execution_allowed" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
