from __future__ import annotations

import unittest

from scripts.select_scorecard_backend import select_backends


class SelectScorecardBackendTests(unittest.TestCase):
    def test_prefers_kaggle_run_approval_over_pruned_colab(self) -> None:
        payload = select_backends(
            {
                "source_preflight": "preflight.json",
                "items": [
                    {
                        "backend": "colab",
                        "status": "ready",
                        "blocker": "No-limit scorecards prune after keepalive errors.",
                    },
                    {
                        "backend": "kaggle",
                        "status": "prepared-needs-run-approval",
                        "blocker": "Ready except explicit run approval.",
                    },
                ],
            }
        )

        self.assertEqual(payload["selected_backend"], "kaggle")
        self.assertFalse(payload["execute"])
        self.assertFalse(payload["promotion_allowed"])

    def test_selection_keeps_required_execution_gates(self) -> None:
        payload = select_backends({"items": [{"backend": "modal", "status": "prepared-needs-credit-and-gpu-policy-check"}]})

        self.assertEqual(payload["status"], "blocked-pending-operator-gates")
        self.assertIn("explicit run approval", payload["required_before_execution"])
        self.assertIn("cost or zero-cost policy confirmation", payload["required_before_execution"])
        self.assertIn("artifact recovery plan", payload["required_before_execution"])

    def test_failed_kaggle_ingest_promotes_modal_as_next_route(self) -> None:
        payload = select_backends(
            {
                "items": [
                    {"backend": "kaggle", "status": "prepared-needs-run-approval", "blocker": "Ready except run approval."},
                    {"backend": "modal", "status": "prepared-needs-credit-and-gpu-policy-check", "blocker": "Needs GPU policy."},
                ],
            },
            {"status": "fail"},
        )

        self.assertEqual(payload["selected_backend"], "modal")
        self.assertIn("Live Kaggle ingest failed", payload["ranked_backends"][1]["blocker"])


if __name__ == "__main__":
    unittest.main()
