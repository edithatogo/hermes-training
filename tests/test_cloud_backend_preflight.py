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

    def test_kaggle_authenticated_with_quota_fallback_is_prepared(self) -> None:
        def fake_run(command: list[str], timeout_s: int = 30) -> dict[str, object]:
            del timeout_s
            if command == ["kaggle", "--version"]:
                return command_result(command, 0, "Kaggle CLI 2.2.1")
            if command == ["kaggle", "config", "view"]:
                return command_result(command, 0, "username: edithatogo\nauth_method: OAUTH")
            if command == ["kaggle", "quota"]:
                return command_result(command, 1, stderr="not enough values to unpack")
            if command == ["kaggle", "kernels", "list", "--mine", "--page-size", "1"]:
                return command_result(command, 0, "Not found")
            raise AssertionError(command)

        quota_fallback = command_result(
            ["kaggle quota sdk fallback"],
            0,
            '{"gpuQuota":{"totalTimeAllowed":"108000s","timeUsed":"0s"}}',
        )
        with (
            patch.object(cloud_backend_preflight, "run_command", side_effect=fake_run),
            patch.object(cloud_backend_preflight, "run_kaggle_quota_sdk_probe", return_value=quota_fallback),
        ):
            summary = cloud_backend_preflight.summarize_kaggle()

        self.assertEqual(summary["status"], "prepared-needs-notebook-contract")
        self.assertEqual(summary["quota"]["returncode"], 1)
        self.assertEqual(summary["quota_sdk_probe"]["returncode"], 0)
        self.assertEqual(summary["kernels"]["returncode"], 0)

    def test_kaggle_authenticated_but_quota_failure_is_gated_without_fallback(self) -> None:
        def fake_run(command: list[str], timeout_s: int = 30) -> dict[str, object]:
            del timeout_s
            if command == ["kaggle", "--version"]:
                return command_result(command, 0, "Kaggle CLI 2.2.1")
            if command == ["kaggle", "config", "view"]:
                return command_result(command, 0, "username: edithatogo\nauth_method: OAUTH")
            if command == ["kaggle", "quota"]:
                return command_result(command, 1, stderr="not enough values to unpack")
            if command == ["kaggle", "kernels", "list", "--mine", "--page-size", "1"]:
                return command_result(command, 0, "Not found")
            raise AssertionError(command)

        quota_fallback = command_result(["kaggle quota sdk fallback"], 1, stderr="fallback failed")
        with (
            patch.object(cloud_backend_preflight, "run_command", side_effect=fake_run),
            patch.object(cloud_backend_preflight, "run_kaggle_quota_sdk_probe", return_value=quota_fallback),
        ):
            summary = cloud_backend_preflight.summarize_kaggle()

        self.assertEqual(summary["status"], "prepared-needs-quota-cli-fix-and-notebook-contract")
        self.assertEqual(summary["kernels"]["returncode"], 0)
        self.assertIn("quota", summary["next_action"])

    def test_colab_summary_exposes_gpu_tpu_policy(self) -> None:
        def fake_run(command: list[str], timeout_s: int = 30) -> dict[str, object]:
            del timeout_s
            if command == ["colab", "version"]:
                return command_result(command, 0, "colab 0.5.11")
            if command == ["colab", "sessions"]:
                return command_result(command, 0, "[colab] No active sessions found on server.")
            raise AssertionError(command)

        with patch.object(cloud_backend_preflight, "run_command", side_effect=fake_run):
            summary = cloud_backend_preflight.summarize_colab()

        self.assertEqual(summary["status"], "ready")
        self.assertTrue(summary["accelerator_policy"]["tpu_requires_opt_in"])
        self.assertIn("scripts/colab_adaptive_train_smoke.py", summary["accelerator_policy"]["tpu_compatible_scripts"])
        self.assertIn("PEFT lm-eval selected-task scorecards", summary["accelerator_policy"]["tpu_incompatible_workloads"])

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

    def test_modal_missing_token_is_blocked(self) -> None:
        def fake_run(command: list[str], timeout_s: int = 30) -> dict[str, object]:
            del timeout_s
            if command == ["modal", "--version"]:
                return command_result(command, 0, "modal client version: 1.5.0")
            if command == ["modal", "profile", "list"]:
                return command_result(command, 0, "")
            if command == ["modal", "token", "info"]:
                return command_result(command, 1, stderr="Token missing")
            raise AssertionError(command)

        with patch.object(cloud_backend_preflight, "run_command", side_effect=fake_run):
            summary = cloud_backend_preflight.summarize_modal()

        self.assertEqual(summary["status"], "blocked-needs-auth")
        self.assertIn("modal token new", summary["next_action"])

    def test_modal_token_info_is_redacted_when_authenticated(self) -> None:
        sensitive_stdout = "Workspace: d-a-mordaunt\nUser: d-a-mordaunt\nToken: super-secret-token-value"

        def fake_run(command: list[str], timeout_s: int = 30) -> dict[str, object]:
            del timeout_s
            if command == ["modal", "--version"]:
                return command_result(command, 0, "modal client version: 1.5.0")
            if command == ["modal", "profile", "list"]:
                return command_result(command, 0, "d-a-mordaunt")
            if command == ["modal", "token", "info"]:
                return command_result(command, 0, sensitive_stdout)
            raise AssertionError(command)

        with patch.object(cloud_backend_preflight, "run_command", side_effect=fake_run):
            summary = cloud_backend_preflight.summarize_modal()

        self.assertEqual(summary["status"], "prepared-needs-credit-and-gpu-policy-check")
        self.assertTrue(summary["token"]["redacted"])
        self.assertNotIn("super-secret-token-value", summary["token"]["stdout"])
        self.assertNotIn("Workspace: d-a-mordaunt", summary["token"]["stdout"])

    def test_lightning_missing_teamspace_owner_is_blocked(self) -> None:
        def fake_run(command: list[str], timeout_s: int = 30) -> dict[str, object]:
            del timeout_s
            if command == ["lightning", "--version"]:
                return command_result(command, 0, "lightning 2026.6.8")
            if command == ["lightning", "studio", "list"]:
                return command_result(command, 0, stderr="Could not find the given Teamspace-Owner None")
            if command == ["lightning", "machine", "list"]:
                return command_result(command, 0, "T4\nL4\nA100")
            raise AssertionError(command)

        with patch.object(cloud_backend_preflight, "run_command", side_effect=fake_run):
            summary = cloud_backend_preflight.summarize_lightning()

        self.assertEqual(summary["status"], "blocked-needs-teamspace-owner")
        self.assertIn("Teamspace owner", summary["next_action"])

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
