from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import cloud_backend_preflight


def command_result(command: list[str], returncode: int, stdout: str = "", stderr: str = "") -> dict[str, object]:
    return {
        "installed": True,
        "path": f"/mock/{command[0]}",
        "command": command,
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
    }


class CloudBackendPreflightTests(unittest.TestCase):
    def test_kaggle_installed_but_unauthenticated_is_blocked(self) -> None:
        def fake_run(command: list[str], timeout_s: int = 30) -> dict[str, object]:
            del timeout_s
            if command == ["kaggle", "--version"]:
                return command_result(command, 0, "Kaggle CLI 2.2.1")
            if command == ["kaggle", "config", "view"]:
                return command_result(command, 1, stderr="Could not find kaggle.json")
            raise AssertionError(command)

        with patch.object(cloud_backend_preflight, "run_command", side_effect=fake_run):
            summary = cloud_backend_preflight.summarize_kaggle()

        self.assertEqual(summary["status"], "blocked-needs-auth")
        self.assertIn("Authenticate Kaggle CLI", summary["next_action"])

    def test_hf_jobs_records_known_credit_blocker(self) -> None:
        def fake_run(command: list[str], timeout_s: int = 30) -> dict[str, object]:
            del timeout_s
            if command == ["hf", "auth", "whoami"]:
                return command_result(command, 0, "edithatogo")
            if command == ["hf", "jobs", "hardware"]:
                return command_result(command, 0, "t4-small")
            if command == ["hf", "jobs", "ps"]:
                return command_result(command, 0, "No jobs found")
            raise AssertionError(command)

        with (
            patch.object(cloud_backend_preflight, "run_command", side_effect=fake_run),
            patch.object(cloud_backend_preflight, "HF_JOBS_SCORECARD_REPORT") as report,
        ):
            report.exists.return_value = True
            report.read_text.return_value = "402 Payment Required\nPre-paid credit balance is insufficient"
            summary = cloud_backend_preflight.summarize_hf_jobs()

        self.assertEqual(summary["status"], "blocked-insufficient-hf-credits")
        self.assertTrue(summary["credit_blocker_observed"])

    def test_write_outputs_skips_timestamp_only_change(self) -> None:
        with TemporaryDirectory() as tmp:
            json_output = Path(tmp) / "backend-preflight.json"
            markdown_output = Path(tmp) / "backend-preflight.md"
            report = {
                "created_at": "2026-06-13T00:00:00+00:00",
                "storage_root": "/Volumes/PortableSSD",
                "storage_root_exists": True,
                "policy": {"no_paid_compute_without_approval": True},
                "backends": {
                    "colab": {
                        "status": "ready",
                        "route": "primary",
                        "stop_condition": "none",
                        "next_action": "run bounded jobs",
                    }
                },
            }

            first_write = cloud_backend_preflight.write_outputs(report, json_output, markdown_output)
            json_before = json_output.read_text(encoding="utf-8")
            markdown_before = markdown_output.read_text(encoding="utf-8")

            updated = dict(report)
            updated["created_at"] = "2026-06-13T00:01:00+00:00"
            second_write = cloud_backend_preflight.write_outputs(updated, json_output, markdown_output)
            json_after = json_output.read_text(encoding="utf-8")
            markdown_after = markdown_output.read_text(encoding="utf-8")

            self.assertEqual(first_write, {"json": True, "markdown": True})
            self.assertEqual(second_write, {"json": False, "markdown": False})
            self.assertEqual(json_before, json_after)
            self.assertEqual(markdown_before, markdown_after)


if __name__ == "__main__":
    unittest.main()
