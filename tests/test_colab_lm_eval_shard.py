from __future__ import annotations

import unittest
from pathlib import Path

from scripts.colab_lm_eval_shard import command_plan, render_markdown


class ColabLmEvalShardTests(unittest.TestCase):
    def test_command_plan_uploads_adapter_config_then_executes_script(self) -> None:
        commands = command_plan(
            session="run-1",
            gpu="T4",
            config=Path("config.json"),
            adapter=Path("adapter.tar.gz"),
            script=Path("runner.py"),
            exec_timeout_s=21600,
        )

        self.assertEqual(commands[0], ["colab", "new", "-s", "run-1", "--gpu", "T4"])
        self.assertEqual(commands[1][-2:], ["adapter.tar.gz", "/content/qwen3-v4-peft-conversion-20260613.tar.gz"])
        self.assertEqual(commands[2][-2:], ["config.json", "/content/qwen3-v4-peft-lm-eval-config.json"])
        self.assertEqual(commands[3], ["colab", "exec", "-s", "run-1", "--file", "runner.py", "--timeout", "21600"])

    def test_render_markdown_includes_recovery_checkpoint(self) -> None:
        markdown = render_markdown(
            {
                "session": "run-1",
                "created_at": "2026-06-13T00:00:00+00:00",
                "mode": "recover",
                "status": "ok",
                "config": "config.json",
                "local_output": "/tmp/run-1",
                "steps": [],
                "recovery": {
                    "summary_status": "running",
                    "summary_checkpoint_phase": "evaluation-running",
                    "summary_result_files": None,
                },
            }
        )

        self.assertIn("evaluation-running", markdown)
        self.assertIn("run-1", markdown)


if __name__ == "__main__":
    unittest.main()
