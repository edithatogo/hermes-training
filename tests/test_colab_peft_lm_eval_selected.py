from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.colab_peft_lm_eval_selected as runner


class ColabPeftLmEvalSelectedTests(unittest.TestCase):
    def test_upload_results_skips_without_results_repo(self) -> None:
        with patch.object(runner, "HF_RESULTS_REPO", None):
            result = runner.upload_results(Path("missing.json"), Path("missing-output"), "run-1")

        self.assertEqual(result["status"], "skipped")

    def test_upload_results_requires_token_when_repo_configured(self) -> None:
        with (
            patch.object(runner, "HF_RESULTS_REPO", "owner/results"),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = runner.upload_results(Path("missing.json"), Path("missing-output"), "run-1")

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["reason"], "HF_TOKEN not set")

    def test_timeout_is_configurable_constant(self) -> None:
        self.assertIsInstance(runner.TIMEOUT_S, int)
        self.assertGreaterEqual(runner.TIMEOUT_S, 1)

    def test_run_command_emits_heartbeat_for_long_process(self) -> None:
        calls: list[float] = []

        result = runner.run_command(
            ["python3", "-c", "import time; time.sleep(0.2); print('done')"],
            timeout_s=5,
            heartbeat_interval_s=0.05,
            heartbeat=calls.append,
        )

        self.assertEqual(result["returncode"], 0)
        self.assertFalse(result["timed_out"])
        self.assertIn("done", result["stdout_tail"])
        self.assertGreaterEqual(len(calls), 1)

    def test_summarize_command_result_omits_stdout_and_stderr(self) -> None:
        summary = runner.summarize_command_result(
            {
                "returncode": 0,
                "timed_out": False,
                "duration_s": 1.2,
                "stdout_tail": "large",
                "stderr_tail": "large",
            }
        )

        self.assertEqual(summary, {"returncode": 0, "timed_out": False, "duration_s": 1.2})


if __name__ == "__main__":
    unittest.main()
