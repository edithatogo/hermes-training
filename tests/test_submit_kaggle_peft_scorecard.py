from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.submit_kaggle_peft_scorecard import (
    KaggleScorecardSpec,
    build_push_command,
    build_report,
    kernel_metadata,
    stage_kernel,
    write_json_report,
)


class SubmitKagglePeftScorecardTests(unittest.TestCase):
    def make_spec(self, staging_dir: Path, runner_path: Path) -> KaggleScorecardSpec:
        return KaggleScorecardSpec(
            run_id="run-1",
            kernel_id="owner/kernel",
            staging_dir=staging_dir,
            runner_path=runner_path,
            timeout_s=3600,
            accelerator="gpu",
            tasks="arc_challenge",
            adapter_repo="owner/adapter",
        )

    def test_kernel_metadata_is_gpu_script_with_internet(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            spec = self.make_spec(Path(tmpdir), Path("runner.py"))

            metadata = kernel_metadata(spec)

        self.assertEqual(metadata["id"], "owner/kernel")
        self.assertEqual(metadata["kernel_type"], "script")
        self.assertTrue(metadata["enable_gpu"])
        self.assertTrue(metadata["enable_internet"])

    def test_stage_kernel_writes_metadata_and_runner(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            runner = Path(tmpdir) / "runner.py"
            runner.write_text("print('ok')\n", encoding="utf-8")
            staging_dir = Path(tmpdir) / "stage"
            spec = self.make_spec(staging_dir, runner)

            staged = stage_kernel(spec)

        self.assertTrue(staged["metadata"].endswith("kernel-metadata.json"))
        self.assertTrue(staged["runner"].endswith("kaggle_peft_lm_eval_selected.py"))

    def test_execute_requires_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            spec = self.make_spec(Path(tmpdir), Path("runner.py"))
            command = build_push_command(spec)

            report = build_report(spec, {}, command, execute=True, confirm_kaggle_run=False)

        self.assertEqual(report["status"], "blocked")
        self.assertTrue(report["blockers"])

    def test_execute_blocks_when_auth_blocker_is_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            spec = self.make_spec(Path(tmpdir), Path("runner.py"))
            command = build_push_command(spec)

            report = build_report(
                spec,
                {},
                command,
                execute=True,
                confirm_kaggle_run=True,
                auth_blocker_observed=True,
            )

        self.assertEqual(report["status"], "blocked")
        self.assertIn("known Kaggle authentication blocker", report["blockers"][0])

    def test_execute_can_override_stale_auth_blocker_after_manual_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            spec = self.make_spec(Path(tmpdir), Path("runner.py"))
            command = build_push_command(spec)

            report = build_report(
                spec,
                {},
                command,
                execute=True,
                confirm_kaggle_run=True,
                auth_blocker_observed=True,
                ignore_known_auth_blocker=True,
            )

        self.assertEqual(report["status"], "ready-to-submit")
        self.assertFalse(report["blockers"])

    def test_write_json_report_persists_updated_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "report.json"
            report = {"status": "ready-to-submit"}
            write_json_report(path, report)
            report["submission"] = {"returncode": 0}
            write_json_report(path, report)

            text = path.read_text(encoding="utf-8")

        self.assertIn('"submission"', text)
        self.assertIn('"returncode": 0', text)


if __name__ == "__main__":
    unittest.main()
