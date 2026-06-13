from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_kaggle_result_ingest import validate_ingest


class ValidateKaggleResultIngestTests(unittest.TestCase):
    def make_successful_run(self, root: Path) -> Path:
        run_dir = root / "hermes-evals" / "kaggle" / "run-1"
        output_dir = run_dir / "lm-eval-output"
        output_dir.mkdir(parents=True)
        (output_dir / "results.json").write_text(
            json.dumps(
                {
                    "results": {
                        "arc_challenge": {"acc,none": 0.1},
                        "hellaswag": {"acc,none": 0.2},
                        "truthfulqa_mc2": {"acc,none": 0.3},
                        "gsm8k": {"exact_match,strict-match": 0.4},
                        "winogrande": {"acc,none": 0.5},
                    }
                }
            ),
            encoding="utf-8",
        )
        summary = run_dir / "summary.json"
        summary.write_text(
            json.dumps(
                {
                    "status": "scored",
                    "adapter_repo": "edithatogo/qwen3-4b-hermes-lora-peft-converted",
                    "base_model": "Qwen/Qwen3-4B",
                    "tasks": "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande",
                    "limit": None,
                    "output_dir": str(output_dir),
                    "evaluation": {
                        "returncode": 0,
                        "timed_out": False,
                        "command": ["python", "-m", "lm_eval", "--tasks", "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"],
                    },
                }
            ),
            encoding="utf-8",
        )
        return summary

    def test_pending_artifacts_passes_in_allow_pending_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            report = validate_ingest(root / "missing-summary.json", root, allow_pending=True)

        self.assertEqual(report["status"], "pending_artifacts")
        self.assertTrue(report["checks"][0]["passed"])

    def test_successful_no_limit_run_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = self.make_successful_run(root)

            report = validate_ingest(summary, root.resolve(), allow_pending=False)

        self.assertEqual(report["status"], "pass")
        self.assertEqual(set(report["found_tasks"]), {"arc_challenge", "hellaswag", "truthfulqa_mc2", "gsm8k", "winogrande"})

    def test_limited_run_fails_claim_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = self.make_successful_run(root)
            payload = json.loads(summary.read_text(encoding="utf-8"))
            payload["limit"] = "10"
            payload["evaluation"]["command"].extend(["--limit", "10"])
            summary.write_text(json.dumps(payload), encoding="utf-8")

            report = validate_ingest(summary, root.resolve(), allow_pending=False)

        self.assertEqual(report["status"], "fail")
        self.assertFalse(next(check for check in report["checks"] if check["name"] == "no_limit_configured")["passed"])
        self.assertFalse(next(check for check in report["checks"] if check["name"] == "command_has_no_limit_flag")["passed"])


if __name__ == "__main__":
    unittest.main()
