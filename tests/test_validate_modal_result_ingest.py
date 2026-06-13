from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_modal_result_ingest import validate_ingest


class ValidateModalResultIngestTests(unittest.TestCase):
    def test_pending_artifacts_passes_in_allow_pending_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            report = validate_ingest(root / "missing-modal-result.json", allow_pending=True)

        self.assertEqual(report["status"], "pending_artifacts")
        self.assertTrue(report["checks"][0]["passed"])

    def test_successful_modal_result_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result_path = Path(tmp) / "modal-result.json"
            result_path.write_text(
                json.dumps(
                    {
                        "status": "scored",
                        "adapter_repo": "edithatogo/qwen3-4b-hermes-lora-peft-converted",
                        "base_model": "Qwen/Qwen3-4B",
                        "tasks": "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande",
                        "limit": None,
                        "evaluation": {
                            "returncode": 0,
                            "timed_out": False,
                            "command": ["python", "-m", "lm_eval", "--tasks", "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"],
                        },
                        "result_files": [
                            "arc_challenge/results.json",
                            "hellaswag/results.json",
                            "truthfulqa_mc2/results.json",
                            "gsm8k/results.json",
                            "winogrande/results.json",
                        ],
                    }
                ),
                encoding="utf-8",
            )

            report = validate_ingest(result_path, allow_pending=False)

        self.assertEqual(report["status"], "pass")

    def test_nonzero_result_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result_path = Path(tmp) / "modal-result.json"
            result_path.write_text(
                json.dumps(
                    {
                        "status": "blocked",
                        "adapter_repo": "edithatogo/qwen3-4b-hermes-lora-peft-converted",
                        "base_model": "Qwen/Qwen3-4B",
                        "tasks": "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande",
                        "limit": None,
                        "evaluation": {"returncode": 1, "timed_out": False, "command": ["python", "-m", "lm_eval"]},
                        "result_files": [],
                    }
                ),
                encoding="utf-8",
            )

            report = validate_ingest(result_path, allow_pending=False)

        self.assertEqual(report["status"], "fail")


if __name__ == "__main__":
    unittest.main()
