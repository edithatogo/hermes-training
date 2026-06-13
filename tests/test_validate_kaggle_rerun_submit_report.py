from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_kaggle_rerun_submit_report import validate_report, validate_status_report, validate_v3_report


class ValidateKaggleRerunSubmitReportTests(unittest.TestCase):
    def test_rejects_unconfirmed_or_promotional_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            report.write_text(
                json.dumps(
                    {
                        "backend": "kaggle-kernels",
                        "execute": False,
                        "confirm_kaggle_run": False,
                        "status": "dry-run",
                        "torch_compatibility_policy": "default",
                        "use_4bit": True,
                        "blockers": [],
                        "submission": {"returncode": 0, "stdout": "Kernel version 2 successfully pushed"},
                        "claim_boundary": "promoted",
                    }
                ),
                encoding="utf-8",
            )

            failures = validate_report(report)

        self.assertTrue(any("explicit execute" in failure for failure in failures))
        self.assertTrue(any("p100-cu118" in failure for failure in failures))
        self.assertTrue(any("non-promotional claim boundary" in failure for failure in failures))

    def test_accepts_v3_submission_version_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            report.write_text(
                json.dumps(
                    {
                        "backend": "kaggle-kernels",
                        "execute": True,
                        "confirm_kaggle_run": True,
                        "status": "ready-to-submit",
                        "torch_compatibility_policy": "p100-cu118",
                        "use_4bit": False,
                        "blockers": [],
                        "submission": {"returncode": 0, "stdout": "Kernel version 3 successfully pushed"},
                        "claim_boundary": "No-limit benchmark claim only after Kaggle completes every configured task without --limit.",
                    }
                ),
                encoding="utf-8",
            )

            failures = validate_v3_report(report)

        self.assertEqual(failures, [])

    def test_rejects_status_report_with_incomplete_failure_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "status.json"
            report.write_text(
                json.dumps(
                    {
                        "kernel_id": "edithatogo/qwen3-v4-peft-lm-eval-selected-full",
                        "status": "KernelWorkerStatus.COMPLETE",
                        "downloaded_file_count": 3,
                        "artifact_dir": "/tmp/not-ssd",
                        "claim_boundary": "promoted",
                        "failure_summary": "status=blocked",
                    }
                ),
                encoding="utf-8",
            )

            failures = validate_status_report(report)

        self.assertTrue(any("recovered file count" in failure for failure in failures))
        self.assertTrue(any("SSD" in failure for failure in failures))
        self.assertTrue(any("non-promotional claim boundary" in failure for failure in failures))
        self.assertTrue(any("evaluation.returncode=1" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
