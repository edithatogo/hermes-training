from __future__ import annotations

import unittest

from scripts.submit_hf_jobs_peft_scorecard import HfJobsScorecardSpec, build_job_command, build_report


class SubmitHfJobsPeftScorecardTests(unittest.TestCase):
    def test_command_mounts_adapter_and_passes_result_repo(self) -> None:
        spec = HfJobsScorecardSpec(
            run_id="run-1",
            results_repo="owner/results",
            adapter_repo="owner/adapter",
            flavor="t4-small",
            timeout="8h",
            image="image:tag",
            tasks="arc_challenge",
            script_url="https://example.test/script.py",
        )

        command = build_job_command(spec)

        self.assertIn("hf://models/owner/adapter:/adapter:ro", command)
        self.assertIn("RUN_ID=run-1", command)
        self.assertIn("HF_RESULTS_REPO=owner/results", command)
        self.assertIn("LM_EVAL_TASKS=arc_challenge", command)
        self.assertIn("--detach", command)

    def test_execute_requires_paid_compute_confirmation(self) -> None:
        spec = HfJobsScorecardSpec(
            run_id="run-1",
            results_repo="owner/results",
            adapter_repo="owner/adapter",
            flavor="t4-small",
            timeout="8h",
            image="image:tag",
            tasks="arc_challenge",
            script_url="https://example.test/script.py",
        )

        report = build_report(spec, build_job_command(spec), execute=True, confirm_paid_compute=False)

        self.assertEqual(report["status"], "blocked")
        self.assertTrue(report["blockers"])

    def test_execute_blocks_when_credit_blocker_is_recorded(self) -> None:
        spec = HfJobsScorecardSpec(
            run_id="run-1",
            results_repo="owner/results",
            adapter_repo="owner/adapter",
            flavor="t4-small",
            timeout="8h",
            image="image:tag",
            tasks="arc_challenge",
            script_url="https://example.test/script.py",
        )

        report = build_report(
            spec,
            build_job_command(spec),
            execute=True,
            confirm_paid_compute=True,
            credit_blocker_observed=True,
        )

        self.assertEqual(report["status"], "blocked")
        self.assertIn("known HF Jobs prepaid credit blocker", report["blockers"][0])

    def test_execute_can_override_stale_credit_blocker_after_manual_verification(self) -> None:
        spec = HfJobsScorecardSpec(
            run_id="run-1",
            results_repo="owner/results",
            adapter_repo="owner/adapter",
            flavor="t4-small",
            timeout="8h",
            image="image:tag",
            tasks="arc_challenge",
            script_url="https://example.test/script.py",
        )

        report = build_report(
            spec,
            build_job_command(spec),
            execute=True,
            confirm_paid_compute=True,
            credit_blocker_observed=True,
            ignore_known_credit_blocker=True,
        )

        self.assertEqual(report["status"], "ready-to-submit")
        self.assertFalse(report["blockers"])


if __name__ == "__main__":
    unittest.main()
