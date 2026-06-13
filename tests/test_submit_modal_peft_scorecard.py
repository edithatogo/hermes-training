from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.submit_modal_peft_scorecard import (
    ModalScorecardSpec,
    build_modal_command,
    build_report,
    stage_config,
    write_json_report,
)


class SubmitModalPeftScorecardTests(unittest.TestCase):
    def make_spec(self, staging_dir: Path) -> ModalScorecardSpec:
        return ModalScorecardSpec(
            run_id="run-1",
            staging_dir=staging_dir,
            app_path=Path("scripts/modal_peft_lm_eval_selected.py"),
            timeout_s=3600,
            gpu="T4",
            tasks="arc_challenge",
            adapter_repo="owner/adapter",
        )

    def test_modal_command_targets_scorecard_function(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.make_spec(Path(tmp))

            command = build_modal_command(spec)

        self.assertEqual(command[:2], ["modal", "run"])
        self.assertIn("scripts/modal_peft_lm_eval_selected.py::scorecard", command)
        self.assertIn("--config-json", command)

    def test_stage_config_writes_modal_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.make_spec(Path(tmp))

            staged = stage_config(spec)

            self.assertTrue(staged["config"].endswith("modal-peft-lm-eval-config.json"))
            self.assertTrue(Path(staged["config"]).exists())

    def test_execute_requires_modal_and_zero_cost_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.make_spec(Path(tmp))
            command = build_modal_command(spec)

            report = build_report(
                spec,
                {},
                command,
                execute=True,
                confirm_modal_run=False,
                confirm_zero_cost_compute=False,
            )

        self.assertEqual(report["status"], "blocked")
        self.assertIn("--confirm-modal-run", report["blockers"][0])
        self.assertIn("--confirm-zero-cost-compute", report["blockers"][1])

    def test_execute_blocks_when_policy_gate_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.make_spec(Path(tmp))
            command = build_modal_command(spec)

            report = build_report(
                spec,
                {},
                command,
                execute=True,
                confirm_modal_run=True,
                confirm_zero_cost_compute=True,
                modal_policy_gate_observed=True,
            )

        self.assertEqual(report["status"], "blocked")
        self.assertIn("Modal backend preflight", report["blockers"][0])

    def test_write_json_report_persists_updated_submission(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "modal-report.json"
            report = {"status": "ready-to-submit"}
            write_json_report(path, report)
            report["submission"] = {"returncode": 0}
            write_json_report(path, report)

            text = path.read_text(encoding="utf-8")

        self.assertIn('"submission"', text)
        self.assertIn('"returncode": 0', text)


if __name__ == "__main__":
    unittest.main()
