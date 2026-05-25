from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER = REPO_ROOT / "scripts" / "run_qwen3_onnx_transformersjs_smoke.py"


def run_runner(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("HERMES_STORAGE_ROOT", None)
    env.pop("HERMES_EVAL_ROOT", None)
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def extract_reported_path(stdout: str, key: str) -> Path:
    patterns = (
        rf"(?im)^{re.escape(key)}\s*[:=]\s*(?P<value>.+?)\s*$",
        rf"(?im)^{re.escape(key.replace('_', '-'))}\s*[:=]\s*(?P<value>.+?)\s*$",
        rf'"{re.escape(key)}"\s*:\s*"(?P<value>[^"]+)"',
        rf"'{re.escape(key)}'\s*:\s*'(?P<value>[^']+)'",
    )
    for pattern in patterns:
        match = re.search(pattern, stdout)
        if match:
            return Path(match.group("value").strip())
    raise AssertionError(f"could not find {key!r} in runner output:\n{stdout}")


class Qwen3OnnxTransformersJsSmokeTests(unittest.TestCase):
    def test_dry_run_accepts_explicit_paths_and_run_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tool_root = Path(tmp) / "tool-root"
            output_root = Path(tmp) / "output-root"

            result = run_runner(
                "--dry-run",
                "--model-id",
                "onnx-community/Qwen3-Reranker-0.6B-ONNX",
                "--tool-root",
                str(tool_root),
                "--output-root",
                str(output_root),
                "--run-id",
                "qwen3-onnx-smoke-test",
            )

        self.assertEqual(result.returncode, 0, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        self.assertIn("onnx-community/Qwen3-Reranker-0.6B-ONNX", result.stdout)
        self.assertIn("qwen3-onnx-smoke-test", result.stdout)
        self.assertIn(str(tool_root), result.stdout)
        self.assertIn(str(output_root), result.stdout)

    def test_default_paths_stay_on_portable_ssd_and_outside_repo(self) -> None:
        repo_node_modules = REPO_ROOT / "node_modules"
        existed_before = repo_node_modules.exists()

        result = run_runner(
            "--dry-run",
            "--model-id",
            "onnx-community/Qwen3-Reranker-0.6B-ONNX",
            "--run-id",
            "qwen3-onnx-defaults-test",
        )

        self.assertEqual(result.returncode, 0, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")

        tool_root = extract_reported_path(result.stdout, "tool_root")
        output_root = extract_reported_path(result.stdout, "output_root")

        self.assertTrue(tool_root.is_absolute(), tool_root)
        self.assertTrue(output_root.is_absolute(), output_root)
        self.assertTrue(str(tool_root).startswith("/Volumes/PortableSSD"), tool_root)
        self.assertTrue(str(output_root).startswith("/Volumes/PortableSSD"), output_root)
        self.assertFalse(tool_root.is_relative_to(REPO_ROOT), tool_root)
        self.assertFalse(output_root.is_relative_to(REPO_ROOT), output_root)
        self.assertEqual(repo_node_modules.exists(), existed_before)

    def test_dry_run_accepts_coreml_device(self) -> None:
        result = run_runner(
            "--dry-run",
            "--device",
            "coreml",
            "--run-id",
            "qwen3-onnx-coreml-test",
        )

        self.assertEqual(result.returncode, 0, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        self.assertIn('"device": "coreml"', result.stdout)


if __name__ == "__main__":
    unittest.main()
