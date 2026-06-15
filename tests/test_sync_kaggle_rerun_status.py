from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sync_kaggle_rerun_status import build_status_report, parse_status


class SyncKaggleRerunStatusTests(unittest.TestCase):
    def test_parse_status_extracts_kernel_worker_state(self) -> None:
        stdout = 'edithatogo/qwen3-v4-peft-lm-eval-selected-full has status "KernelWorkerStatus.RUNNING"'

        self.assertEqual(parse_status(stdout), "KernelWorkerStatus.RUNNING")

    def test_running_report_keeps_claims_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = build_status_report(
                kernel_id="owner/kernel",
                kernel_version=7,
                artifact_dir=Path(tmp) / "artifacts",
                status_result={
                    "command": ["kaggle", "kernels", "status", "owner/kernel"],
                    "stdout": 'owner/kernel has status "KernelWorkerStatus.RUNNING"',
                    "stderr": "",
                    "returncode": 0,
                },
            )

        self.assertEqual(report["status"], "KernelWorkerStatus.RUNNING")
        self.assertEqual(report["downloaded_file_count"], 0)
        self.assertIn("No benchmark claim", report["claim_boundary"])
        self.assertIn("artifact recovery", report["running_summary"])

    def test_complete_report_detects_recovered_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifacts"
            artifact_dir.mkdir()
            summary = artifact_dir / "run-summary.json"
            summary.write_text(json.dumps({"status": "scored"}), encoding="utf-8")

            report = build_status_report(
                kernel_id="owner/kernel",
                kernel_version=7,
                artifact_dir=artifact_dir,
                status_result={
                    "command": ["kaggle", "kernels", "status", "owner/kernel"],
                    "stdout": 'owner/kernel has status "KernelWorkerStatus.COMPLETE"',
                    "stderr": "",
                    "returncode": 0,
                },
            )

        self.assertEqual(report["status"], "KernelWorkerStatus.COMPLETE")
        self.assertEqual(report["downloaded_file_count"], 1)
        self.assertEqual(report["recovered_summary"], str(summary))
        self.assertEqual(report["recovered_summary_status"], "scored")
        self.assertIn("no-pending", report["claim_boundary"])
        self.assertIn("status=scored", report["failure_summary"])


if __name__ == "__main__":
    unittest.main()
