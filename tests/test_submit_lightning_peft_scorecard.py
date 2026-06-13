from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.submit_lightning_peft_scorecard import (
    TEAMSPACE_PLACEHOLDER,
    LightningScorecardSpec,
    build_lightning_command,
    build_report,
    stage_config,
)


class SubmitLightningPeftScorecardTests(unittest.TestCase):
    def make_spec(self, staging_dir: Path, teamspace: str = TEAMSPACE_PLACEHOLDER) -> LightningScorecardSpec:
        return LightningScorecardSpec(
            run_id="run-1",
            staging_dir=staging_dir,
            teamspace=teamspace,
            machine="T4",
            image="pytorch/pytorch:2.7.1-cuda12.6-cudnn9-runtime",
            script_url="https://example.test/script.py",
            tasks="arc_challenge",
            adapter_repo="owner/adapter",
            timeout_s=3600,
        )

    def test_lightning_command_uses_job_run_with_teamspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.make_spec(Path(tmp), teamspace="owner/team")

            command = build_lightning_command(spec)

        self.assertEqual(command[:3], ["lightning", "job", "run"])
        self.assertIn("--teamspace", command)
        self.assertIn("owner/team", command)
        self.assertIn("--machine", command)
        self.assertIn("T4", command)

    def test_stage_config_writes_lightning_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.make_spec(Path(tmp))

            staged = stage_config(spec)

            self.assertTrue(staged["config"].endswith("lightning-peft-lm-eval-config.json"))
            self.assertTrue(Path(staged["config"]).exists())

    def test_execute_requires_confirmations_and_real_teamspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.make_spec(Path(tmp))
            command = build_lightning_command(spec)

            report = build_report(
                spec,
                {},
                command,
                execute=True,
                confirm_lightning_run=False,
                confirm_zero_cost_compute=False,
            )

        self.assertEqual(report["status"], "blocked")
        self.assertTrue(any("--confirm-lightning-run" in blocker for blocker in report["blockers"]))
        self.assertTrue(any("--confirm-zero-cost-compute" in blocker for blocker in report["blockers"]))
        self.assertTrue(any("--teamspace" in blocker for blocker in report["blockers"]))

    def test_execute_blocks_on_known_teamspace_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.make_spec(Path(tmp), teamspace="owner/team")
            command = build_lightning_command(spec)

            report = build_report(
                spec,
                {},
                command,
                execute=True,
                confirm_lightning_run=True,
                confirm_zero_cost_compute=True,
                teamspace_blocker_observed=True,
            )

        self.assertEqual(report["status"], "blocked")
        self.assertIn("known Lightning teamspace blocker", report["blockers"][0])


if __name__ == "__main__":
    unittest.main()
