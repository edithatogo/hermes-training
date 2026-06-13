from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.hf_jobs_peft_lm_eval_selected import resolve_adapter_dir


class HfJobsPeftLmEvalSelectedTests(unittest.TestCase):
    def test_existing_adapter_dir_is_used_without_download(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter_dir = Path(tmpdir)

            resolved = resolve_adapter_dir(adapter_dir)

        self.assertEqual(resolved, adapter_dir)

    def test_missing_adapter_dir_can_download_from_repo_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "adapter"
            missing = Path(tmpdir) / "missing"

            with (
                patch.dict(
                    "os.environ",
                    {"PEFT_ADAPTER_REPO": "owner/repo", "PEFT_ADAPTER_DOWNLOAD_DIR": str(target)},
                    clear=False,
                ),
                patch("huggingface_hub.snapshot_download") as snapshot_download,
            ):
                snapshot_download.return_value = str(target)
                resolved = resolve_adapter_dir(missing)

        self.assertEqual(resolved, target)
        snapshot_download.assert_called_once()


if __name__ == "__main__":
    unittest.main()
