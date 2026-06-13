from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_kaggle_kernel_contract import validate_contract


class ValidateKaggleKernelContractTests(unittest.TestCase):
    def make_contract_files(self, root: Path) -> tuple[Path, Path, Path]:
        staging = root / "stage"
        staging.mkdir()
        (staging / "kernel-metadata.json").write_text(
            json.dumps(
                {
                    "id": "edithatogo/qwen3-v4-peft-lm-eval-selected-full",
                    "kernel_type": "script",
                    "language": "python",
                    "enable_gpu": True,
                    "enable_internet": True,
                    "is_private": False,
                    "license": "apache-2.0",
                }
            ),
            encoding="utf-8",
        )
        (staging / "kaggle-peft-lm-eval-config.json").write_text(
            json.dumps(
                {
                    "adapter_repo": "edithatogo/qwen3-4b-hermes-lora-peft-converted",
                    "limit": None,
                    "tasks": "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande",
                    "timeout_s": 21600,
                    "torch_compatibility_policy": "p100-cu118",
                    "use_4bit": False,
                }
            ),
            encoding="utf-8",
        )
        (staging / "kaggle_peft_lm_eval_selected.py").write_text(
            "snapshot_download(repo_id=adapter_repo)\n"
            "PEFT_ADAPTER_REPO = 'x'\n"
            "root = '/kaggle/working'\n"
            "result_json = output_dir = root\n"
            "No-limit benchmark claim only if every configured task completes without --limit.\n"
            "policy = 'p100-cu118'\n"
            "index = 'https://download.pytorch.org/whl/cu118'\n",
            encoding="utf-8",
        )
        dry_run = root / "dry-run.json"
        dry_run.write_text(
            json.dumps({"status": "dry-run", "execute": False, "confirm_kaggle_run": False, "blockers": []}),
            encoding="utf-8",
        )
        preflight = root / "preflight.json"
        preflight.write_text(
            json.dumps({"backends": {"kaggle": {"status": "prepared-needs-notebook-contract", "quota_sdk_probe": {"returncode": 0}}}}),
            encoding="utf-8",
        )
        return staging, dry_run, preflight

    def test_contract_passes_for_public_dry_run_kernel(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            staging, dry_run, preflight = self.make_contract_files(Path(tmp))

            report = validate_contract(staging, dry_run, preflight)

        self.assertEqual(report["status"], "pass")
        self.assertFalse(report["dataset_terms_contract"]["private_data_upload"])

    def test_contract_fails_when_kernel_is_private(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            staging, dry_run, preflight = self.make_contract_files(Path(tmp))
            metadata = json.loads((staging / "kernel-metadata.json").read_text(encoding="utf-8"))
            metadata["is_private"] = True
            (staging / "kernel-metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

            report = validate_contract(staging, dry_run, preflight)

        self.assertEqual(report["status"], "fail")
        self.assertFalse(next(check for check in report["checks"] if check["name"] == "metadata_public_kernel")["passed"])


if __name__ == "__main__":
    unittest.main()
