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
        self.assertNotIn("kaggle quota", by_backend["kaggle"]["commands"])
        self.assertIn("./.venv/bin/python scripts/cloud_backend_preflight.py", by_backend["kaggle"]["commands"])
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

    def test_kaggle_contract_and_ingest_gate_derive_run_approval_status(self) -> None:
        items = checklist_items(
            {
                "backends": {
                    "kaggle": {"status": "prepared-needs-notebook-contract"},
                }
            },
            kaggle_contract_report={"status": "pass"},
            kaggle_ingest_report={"status": "pending_artifacts"},
        )
        by_backend = {item["backend"]: item for item in items}

        self.assertEqual(by_backend["kaggle"]["status"], "prepared-needs-run-approval")
        self.assertIn("explicit run approval", by_backend["kaggle"]["blocker"])
        self.assertIn(
            "./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json <downloaded-summary> --no-allow-pending",
            by_backend["kaggle"]["commands"],
        )

    def test_kaggle_submitted_rerun_derives_artifact_recovery_status(self) -> None:
        items = checklist_items(
            {
                "backends": {
                    "kaggle": {"status": "prepared-needs-notebook-contract"},
                }
            },
            kaggle_contract_report={"status": "pass"},
            kaggle_ingest_report={"status": "pending_artifacts"},
            kaggle_rerun_status_report={"status": "KernelWorkerStatus.RUNNING"},
        )
        by_backend = {item["backend"]: item for item in items}

        self.assertEqual(by_backend["kaggle"]["status"], "running-needs-artifact-recovery")
        self.assertIn("artifact recovery", by_backend["kaggle"]["blocker"])
        self.assertIn("version 3", by_backend["kaggle"]["blocker"])
        self.assertIn(
            "kaggle kernels status edithatogo/qwen3-v4-peft-lm-eval-selected-full",
            by_backend["kaggle"]["commands"],
        )
        self.assertTrue(any("kernel-v3" in command for command in by_backend["kaggle"]["commands"]))

    def test_kaggle_completed_failed_rerun_derives_runner_fix_status(self) -> None:
        items = checklist_items(
            {
                "backends": {
                    "kaggle": {"status": "prepared-needs-notebook-contract"},
                }
            },
            kaggle_contract_report={"status": "pass"},
            kaggle_ingest_report={"status": "pending_artifacts"},
            kaggle_rerun_status_report={"status": "KernelWorkerStatus.COMPLETE"},
        )
        by_backend = {item["backend"]: item for item in items}

        self.assertEqual(by_backend["kaggle"]["status"], "completed-failed-needs-kaggle-runner-fix")
        self.assertIn("version 3 completed without scores", by_backend["kaggle"]["blocker"])
        self.assertIn("explicit approval", by_backend["kaggle"]["blocker"])
        self.assertTrue(any("kernel-v3" in command for command in by_backend["kaggle"]["commands"]))
        self.assertIn("./.venv/bin/python scripts/validate_kaggle_rerun_submit_report.py", by_backend["kaggle"]["commands"])

    def test_lightning_includes_guarded_submitter_commands(self) -> None:
        items = checklist_items({"backends": {"lightning": {"status": "blocked-needs-teamspace-owner"}}})
        by_backend = {item["backend"]: item for item in items}

        self.assertIn("./.venv/bin/python scripts/submit_lightning_peft_scorecard.py", by_backend["lightning"]["commands"])
        self.assertIn(
            "./.venv/bin/python scripts/submit_lightning_peft_scorecard.py --teamspace <owner>/<teamspace> --execute --confirm-lightning-run --confirm-zero-cost-compute",
            by_backend["lightning"]["commands"],
        )


if __name__ == "__main__":
    unittest.main()
