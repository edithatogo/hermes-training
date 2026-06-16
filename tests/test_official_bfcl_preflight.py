import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.check_official_bfcl_preflight import EndpointProbe, build_report, render_markdown
from scripts.validate_official_bfcl_preflight import validate_payload


class OfficialBfclPreflightTests(unittest.TestCase):
    def write_queue(self, root: Path) -> Path:
        path = root / "queue.json"
        path.write_text(
            json.dumps(
                {
                    "candidate": "qwen3-4b-strict-toolcall-v4-targeted",
                    "base_model": "Qwen/Qwen3-4B",
                    "adapter": "gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter",
                    "items": [
                        {
                            "suite": "official-bfcl",
                            "status": "missing",
                            "run_id": "qwen3-v4-peft-official-bfcl-20260616",
                            "output_root": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616",
                            "local_command": "bfcl generate --result-dir /tmp/results && bfcl evaluate --score-dir /tmp/scores",
                            "publication_boundary": "No public broad benchmark claim until this suite has scored artifacts and review sign-off.",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return path

    @mock.patch("scripts.check_official_bfcl_preflight.command_version")
    def test_preflight_blocks_without_endpoint_but_keeps_command_ready(self, mocked_command_version: mock.Mock) -> None:
        mocked_command_version.return_value = {
            "path": "/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl",
            "present": True,
            "executable": True,
            "version_output": "usage: bfcl",
        }
        with tempfile.TemporaryDirectory() as tmp:
            report = build_report(queue_path=self.write_queue(Path(tmp)), base_url="", created_at="2026-06-16T00:00:00Z")
        self.assertEqual(report["status"], "blocked-endpoint-preflight")
        self.assertTrue(report["checks"]["bfcl_cli_executable"])
        self.assertFalse(report["checks"]["endpoint_reachable"])
        self.assertEqual(validate_payload(report, Path("report.json")), [])

    @mock.patch("scripts.check_official_bfcl_preflight.command_version")
    @mock.patch("scripts.check_official_bfcl_preflight.probe_endpoint")
    def test_reachable_endpoint_marks_ready_to_run(self, mocked_endpoint: mock.Mock, mocked_command_version: mock.Mock) -> None:
        mocked_command_version.return_value = {
            "path": "/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl",
            "present": True,
            "executable": True,
            "version_output": "usage: bfcl",
        }
        mocked_endpoint.return_value = EndpointProbe(
            base_url="http://127.0.0.1:8080/v1",
            status="reachable",
            detail="GET /v1/models returned JSON.",
            models=["qwen3-v4"],
        )
        with tempfile.TemporaryDirectory() as tmp:
            report = build_report(
                queue_path=self.write_queue(Path(tmp)),
                base_url="http://127.0.0.1:8080/v1",
                created_at="2026-06-16T00:00:00Z",
            )
        self.assertEqual(report["status"], "ready-to-run")
        self.assertEqual(report["blockers"], [])
        self.assertIn("not scored benchmark evidence", report["decision"])

    @mock.patch("scripts.check_official_bfcl_preflight.command_version")
    def test_markdown_preserves_non_score_boundary(self, mocked_command_version: mock.Mock) -> None:
        mocked_command_version.return_value = {
            "path": "/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl",
            "present": True,
            "executable": True,
            "version_output": "usage: bfcl",
        }
        with tempfile.TemporaryDirectory() as tmp:
            markdown = render_markdown(
                build_report(queue_path=self.write_queue(Path(tmp)), base_url="", created_at="2026-06-16T00:00:00Z")
            )
        self.assertIn("does not contain BFCL scores", markdown)
        self.assertIn("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/", markdown)


if __name__ == "__main__":
    unittest.main()
