from __future__ import annotations

import unittest

from scripts.build_cloud_unblock_checklist import checklist_items


class BuildCloudUnblockChecklistTests(unittest.TestCase):
    def test_authenticated_kaggle_and_modal_use_prepared_gates(self) -> None:
        items = checklist_items(
            {
                "backends": {
                    "kaggle": {"status": "prepared-needs-notebook-contract"},
                    "modal": {"status": "prepared-needs-credit-and-gpu-policy-check"},
                }
            }
        )
        by_backend = {item["backend"]: item for item in items}

        self.assertIn("remaining gates", by_backend["kaggle"]["blocker"])
        self.assertNotIn("unauthenticated", by_backend["kaggle"]["blocker"])
        self.assertNotIn("kaggle auth login", by_backend["kaggle"]["commands"])
        self.assertIn("remaining gates", by_backend["modal"]["blocker"])
        self.assertNotIn("no token/profile", by_backend["modal"]["blocker"])
        self.assertNotIn("modal token new", by_backend["modal"]["commands"])

    def test_kaggle_quota_failure_gets_specific_gate(self) -> None:
        items = checklist_items(
            {
                "backends": {
                    "kaggle": {"status": "prepared-needs-quota-cli-fix-and-notebook-contract"},
                }
            }
        )
        by_backend = {item["backend"]: item for item in items}

        self.assertIn("quota", by_backend["kaggle"]["blocker"])
        self.assertIn("kaggle kernels list --mine --page-size 1", by_backend["kaggle"]["commands"])
        self.assertNotIn("kaggle auth login", by_backend["kaggle"]["commands"])


if __name__ == "__main__":
    unittest.main()
