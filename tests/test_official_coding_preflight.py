import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.check_official_coding_preflight import build_report, render_markdown
from scripts.validate_official_coding_preflight import validate_payload


class OfficialCodingPreflightTests(unittest.TestCase):
    def write_queue(self, root: Path, samples: Path) -> Path:
        path = root / "queue.json"
        path.write_text(
            json.dumps(
                {
                    "candidate": "qwen3-4b-strict-toolcall-v4-targeted",
                    "base_model": "Qwen/Qwen3-4B",
                    "adapter": "gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter",
                    "items": [
                        {
                            "suite": "official-coding",
                            "status": "missing",
                            "run_id": "qwen3-v4-peft-official-coding-20260616",
                            "output_root": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616",
                            "local_command": (
                                "/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python "
                                f"-m evalplus.evaluate humaneval --samples {samples} --test-details"
                            ),
                            "publication_boundary": "No public broad benchmark claim until this suite has scored artifacts and review sign-off.",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return path

    @mock.patch("scripts.check_official_coding_preflight.command_status")
    @mock.patch("scripts.check_official_coding_preflight.module_present")
    def test_preflight_blocks_without_generated_solutions(
        self, mocked_module_present: mock.Mock, mocked_command_status: mock.Mock
    ) -> None:
        mocked_command_status.return_value = {
            "path": "/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/evalplus.evaluate",
            "present": True,
            "executable": True,
            "help_output": "NAME evaluate.py",
        }
        mocked_module_present.return_value = True
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            missing_samples = root / "generated.jsonl"
            report = build_report(
                queue_path=self.write_queue(root, missing_samples),
                created_at="2026-06-16T00:00:00Z",
            )
        self.assertEqual(report["status"], "blocked-coding-preflight")
        self.assertFalse(report["checks"]["generated_solutions_present"])
        self.assertTrue(report["checks"]["command_omits_stale_model_flag"])
        self.assertEqual(validate_payload(report, Path("report.json")), [])

    @mock.patch("scripts.check_official_coding_preflight.command_status")
    @mock.patch("scripts.check_official_coding_preflight.module_present")
    def test_generated_jsonl_marks_ready_to_evaluate(
        self, mocked_module_present: mock.Mock, mocked_command_status: mock.Mock
    ) -> None:
        mocked_command_status.return_value = {
            "path": "/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/evalplus.evaluate",
            "present": True,
            "executable": True,
            "help_output": "NAME evaluate.py",
        }
        mocked_module_present.return_value = True
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            samples = root / "generated.jsonl"
            samples.write_text('{"task_id":"HumanEval/0","solution":"def f():\\n    pass"}\n', encoding="utf-8")
            report = build_report(queue_path=self.write_queue(root, samples), created_at="2026-06-16T00:00:00Z")
        self.assertEqual(report["status"], "ready-to-evaluate")
        self.assertEqual(report["blockers"], [])

    @mock.patch("scripts.check_official_coding_preflight.command_status")
    @mock.patch("scripts.check_official_coding_preflight.module_present")
    def test_markdown_preserves_non_score_boundary(
        self, mocked_module_present: mock.Mock, mocked_command_status: mock.Mock
    ) -> None:
        mocked_command_status.return_value = {
            "path": "/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/evalplus.evaluate",
            "present": True,
            "executable": True,
            "help_output": "NAME evaluate.py",
        }
        mocked_module_present.return_value = True
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            markdown = render_markdown(
                build_report(
                    queue_path=self.write_queue(root, root / "generated.jsonl"),
                    created_at="2026-06-16T00:00:00Z",
                )
            )
        self.assertIn("does not contain pass@k scores", markdown)
        self.assertIn("evalplus.evaluate humaneval", markdown)


if __name__ == "__main__":
    unittest.main()
