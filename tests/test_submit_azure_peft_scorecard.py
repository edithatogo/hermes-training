from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.submit_azure_peft_scorecard import AzureScorecardSpec, build_report, build_submit_command


class SubmitAzurePeftScorecardTests(unittest.TestCase):
    def test_command_uses_job_template_workspace_and_compute(self) -> None:
        spec = AzureScorecardSpec(
            run_id="run-1",
            resource_group="rg",
            workspace="ws",
            region="australiaeast",
            compute="azureml:gpu",
            job_template=Path("job.yaml"),
        )

        command = build_submit_command(spec)

        self.assertIn("az", command)
        self.assertIn("ml", command)
        self.assertIn("job", command)
        self.assertIn("create", command)
        self.assertIn("job.yaml", command)
        self.assertIn("rg", command)
        self.assertIn("ws", command)
        self.assertIn("compute=azureml:gpu", command)

    def test_execute_requires_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            template = Path(tmpdir) / "job.yaml"
            template.write_text("type: command\n", encoding="utf-8")
            spec = AzureScorecardSpec(
                run_id="run-1",
                resource_group="rg",
                workspace="ws",
                region="australiaeast",
                compute="azureml:gpu",
                job_template=template,
            )

            with patch("scripts.submit_azure_peft_scorecard.azure_preflight") as preflight:
                preflight.return_value = {
                    "ready": True,
                    "account": {},
                    "ml_extension": {},
                    "template_exists": True,
                    "blockers": [],
                }
                report = build_report(spec, execute=True, confirm_azure_run=False)

        self.assertEqual(report["status"], "blocked")
        self.assertIn("--confirm-azure-run is required with --execute", report["blockers"])


if __name__ == "__main__":
    unittest.main()
