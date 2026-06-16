import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.check_ruler_long_context_preflight import ModuleStatus, build_report, render_markdown
from scripts.validate_ruler_long_context_preflight import validate_payload


class RulerLongContextPreflightTests(unittest.TestCase):
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
                            "suite": "ruler-long-context",
                            "status": "missing",
                            "run_id": "qwen3-v4-peft-ruler-long-context-20260616",
                            "output_root": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616",
                            "local_command": (
                                "/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python "
                                "-m ruler.run --model Qwen/Qwen3-4B "
                                "--adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter "
                                "--tasks niah_single_1 --max_seq_length 4096 "
                                "--output_dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/"
                                "qwen3-v4-peft-ruler-long-context-20260616/ctx4096"
                            ),
                            "publication_boundary": "No public broad benchmark claim until this suite has scored artifacts and review sign-off.",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return path

    @mock.patch("scripts.check_ruler_long_context_preflight.module_status")
    def test_preflight_blocks_without_ruler_module(self, mocked_module_status: mock.Mock) -> None:
        mocked_module_status.return_value = ModuleStatus("ruler", False, "missing")
        with tempfile.TemporaryDirectory() as tmp:
            report = build_report(queue_path=self.write_queue(Path(tmp)), created_at="2026-06-16T00:00:00Z")
        self.assertEqual(report["status"], "blocked-ruler-preflight")
        self.assertFalse(report["checks"]["ruler_module_present"])
        self.assertTrue(report["checks"]["command_uses_initial_context"])
        self.assertEqual(validate_payload(report, Path("report.json")), [])

    @mock.patch("scripts.check_ruler_long_context_preflight.module_status")
    def test_present_ruler_module_marks_ready(self, mocked_module_status: mock.Mock) -> None:
        mocked_module_status.return_value = ModuleStatus("ruler", True, "/tmp/ruler.py")
        with tempfile.TemporaryDirectory() as tmp:
            report = build_report(queue_path=self.write_queue(Path(tmp)), created_at="2026-06-16T00:00:00Z")
        self.assertEqual(report["status"], "ready-to-run")
        self.assertEqual(report["blockers"], [])

    @mock.patch("scripts.check_ruler_long_context_preflight.module_status")
    def test_markdown_records_context_ladder_and_boundary(self, mocked_module_status: mock.Mock) -> None:
        mocked_module_status.return_value = ModuleStatus("ruler", False, "missing")
        with tempfile.TemporaryDirectory() as tmp:
            markdown = render_markdown(
                build_report(queue_path=self.write_queue(Path(tmp)), created_at="2026-06-16T00:00:00Z")
            )
        self.assertIn("Context ladder", markdown)
        self.assertIn("does not contain RULER scores", markdown)
        self.assertIn("ctx4096", markdown)


if __name__ == "__main__":
    unittest.main()
