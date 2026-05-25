#!/usr/bin/env python3
"""Smoke-test the isolated official benchmark Python environments.

Run this script with the interpreter from the environment being checked.
It verifies imports, package versions, `pip check`, and selected CLI entrypoints
without downloading benchmark data or running model inference.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.metadata as metadata
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


MODES = {
    "general": {
        "imports": (
            "lm_eval",
            "langdetect",
            "immutabledict",
            "evaluate",
            "evalplus",
            "human_eval",
            "mteb",
            "sentence_transformers",
            "transformers",
            "torch",
        ),
        "distributions": (
            "lm_eval",
            "langdetect",
            "immutabledict",
            "evaluate",
            "evalplus",
            "human-eval",
            "mteb",
            "torch",
            "transformers",
            "sentence-transformers",
            "tree-sitter",
        ),
        "cli": (("lm_eval", "--help"),),
    },
    "bfcl": {
        "imports": (
            "bfcl_eval",
            "soundfile",
            "tree_sitter",
            "numpy",
            "torch",
            "transformers",
            "sentence_transformers",
        ),
        "distributions": (
            "bfcl-eval",
            "soundfile",
            "tree-sitter",
            "numpy",
            "torch",
            "transformers",
            "sentence-transformers",
        ),
        "cli": (("bfcl", "--help"),),
    },
}


def check_imports(names: tuple[str, ...]) -> dict[str, str]:
    results: dict[str, str] = {}
    for name in names:
        try:
            importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001
            results[name] = f"fail: {type(exc).__name__}: {exc}"
        else:
            results[name] = "ok"
    return results


def package_versions(names: tuple[str, ...]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in names:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = "missing"
    return versions


def run_command(command: tuple[str, ...]) -> dict[str, Any]:
    env = os.environ.copy()
    env["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{env.get('PATH', '')}"
    resolved = list(command)
    executable = Path(sys.executable).parent / command[0]
    if executable.exists():
        resolved[0] = str(executable)
    result = subprocess.run(resolved, capture_output=True, text=True, timeout=30, env=env)
    return {
        "command": resolved,
        "returncode": result.returncode,
        "stdout_head": result.stdout[:400],
        "stderr_head": result.stderr[:400],
    }


def smoke(mode: str) -> dict[str, Any]:
    cfg = MODES[mode]
    pip_check = run_command((sys.executable, "-m", "pip", "check"))
    cli_results = [run_command(command) for command in cfg["cli"]]

    mps_available = None
    try:
        import torch

        mps_available = bool(torch.backends.mps.is_available())
    except Exception:  # noqa: BLE001
        mps_available = None

    result = {
        "mode": mode,
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "imports": check_imports(cfg["imports"]),
        "versions": package_versions(cfg["distributions"]),
        "pip_check": pip_check,
        "cli": cli_results,
        "torch_mps_available": mps_available,
    }
    result["ok"] = all(value == "ok" for value in result["imports"].values())
    result["ok"] = result["ok"] and all(value != "missing" for value in result["versions"].values())
    result["ok"] = result["ok"] and pip_check["returncode"] == 0
    result["ok"] = result["ok"] and all(item["returncode"] == 0 for item in cli_results)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=sorted(MODES), required=True)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    result = smoke(args.mode)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
