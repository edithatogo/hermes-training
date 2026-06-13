from __future__ import annotations

import unittest

from scripts.submit_ngc_cloud_function_scorecard import (
    DEFAULT_CONTAINER_IMAGE,
    DEFAULT_GPU_SPEC,
    NgcCloudFunctionScorecardSpec,
    build_report,
    build_task_command,
)


class SubmitNgcCloudFunctionScorecardTests(unittest.TestCase):
    def make_spec(
        self,
        container_image: str = "org/team/hermes-scorecard:20260613",
        gpu_specification: str = "L40S:1g",
    ) -> NgcCloudFunctionScorecardSpec:
        return NgcCloudFunctionScorecardSpec(
            run_id="run-1",
            task_name="task-1",
            adapter_repo="owner/adapter",
            tasks="arc_challenge",
            container_image=container_image,
            gpu_specification=gpu_specification,
            max_runtime_duration="6H",
        )

    def test_command_builds_cloud_function_task(self) -> None:
        spec = self.make_spec()

        command = build_task_command(spec)

        self.assertEqual(command[:4], ["ngc", "cloud-function", "task", "create"])
        self.assertIn("org/team/hermes-scorecard:20260613", command)
        self.assertIn("RUN_ID:run-1", command)
        self.assertIn("PEFT_ADAPTER_REPO:owner/adapter", command)
        self.assertIn("LM_EVAL_TASKS:arc_challenge", command)

    def test_execute_requires_confirmation(self) -> None:
        spec = self.make_spec()

        report = build_report(
            spec,
            build_task_command(spec),
            execute=True,
            confirm_ngc_run=False,
        )

        self.assertEqual(report["status"], "blocked")
        self.assertIn("--confirm-ngc-run is required with --execute", report["blockers"])

    def test_execute_blocks_on_known_auth_blocker(self) -> None:
        spec = self.make_spec()

        report = build_report(
            spec,
            build_task_command(spec),
            execute=True,
            confirm_ngc_run=True,
            auth_blocker_observed=True,
        )

        self.assertEqual(report["status"], "blocked")
        self.assertIn("known NGC auth/entitlement blocker", report["blockers"][0])

    def test_execute_blocks_on_placeholder_container_and_gpu(self) -> None:
        spec = self.make_spec(container_image=DEFAULT_CONTAINER_IMAGE, gpu_specification=DEFAULT_GPU_SPEC)

        report = build_report(
            spec,
            build_task_command(spec),
            execute=True,
            confirm_ngc_run=True,
            auth_blocker_observed=False,
        )

        self.assertEqual(report["status"], "blocked")
        self.assertEqual(len(report["blockers"]), 2)

    def test_execute_can_override_stale_auth_blocker_after_manual_verification(self) -> None:
        spec = self.make_spec()

        report = build_report(
            spec,
            build_task_command(spec),
            execute=True,
            confirm_ngc_run=True,
            auth_blocker_observed=True,
            ignore_known_auth_blocker=True,
        )

        self.assertEqual(report["status"], "ready-to-submit")
        self.assertFalse(report["blockers"])


if __name__ == "__main__":
    unittest.main()
