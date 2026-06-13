from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_modal_scorecard_contract import validate_contract


class ValidateModalScorecardContractTests(unittest.TestCase):
    def make_contract_files(self, root: Path) -> tuple[Path, Path, Path]:
        staging = root / "stage"
        staging.mkdir()
        (staging / "modal-peft-lm-eval-config.json").write_text(
            json.dumps(
                {
                    "adapter_repo": "edithatogo/qwen3-4b-hermes-lora-peft-converted",
                    "base_model": "Qwen/Qwen3-4B",
                    "limit": None,
                    "tasks": "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande",
                    "timeout_s": 21600,
                    "output_dir": "/results/run/lm-eval-output",
                    "result_json": "/results/run/summary.json",
                }
            ),
            encoding="utf-8",
        )
        dry_run = root / "modal-dry-run.json"
        dry_run.write_text(
            json.dumps(
                {
                    "status": "dry-run",
                    "execute": False,
                    "confirm_modal_run": False,
                    "confirm_zero_cost_compute": False,
                    "blockers": [],
                    "command": ["modal", "run", "--write-result", "modal-result.json", "app.py::scorecard"],
                }
            ),
            encoding="utf-8",
        )
        app = root / "app.py"
        app.write_text(
            '@app.function(image=image, gpu="T4", timeout=21600, volumes={"/results": results_volume})\n'
            "results_volume = modal.Volume.from_name('x')\n"
            "results_volume.commit()\n"
            "No-limit benchmark claim only if every configured task completes without --limit.\n",
            encoding="utf-8",
        )
        return staging, dry_run, app

    def test_contract_passes_for_fail_closed_modal_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            staging, dry_run, app = self.make_contract_files(Path(tmp))

            report = validate_contract(staging, dry_run, app)

        self.assertEqual(report["status"], "pass")

    def test_contract_fails_when_dry_run_executes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            staging, dry_run, app = self.make_contract_files(Path(tmp))
            payload = json.loads(dry_run.read_text(encoding="utf-8"))
            payload["execute"] = True
            dry_run.write_text(json.dumps(payload), encoding="utf-8")

            report = validate_contract(staging, dry_run, app)

        self.assertEqual(report["status"], "fail")
        self.assertFalse(next(check for check in report["checks"] if check["name"] == "dry_run_no_execute")["passed"])


if __name__ == "__main__":
    unittest.main()
