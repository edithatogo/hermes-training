#!/usr/bin/env python3
"""Validate the pinned safety/refusal manifest and queue command."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from run_tool_call_benchmark import validate_suite
except ModuleNotFoundError:  # pragma: no cover - package import path for tests
    from scripts.run_tool_call_benchmark import validate_suite


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUITE = ROOT / "reports/benchmark/manifests/safety-refusal-suite-20260616.json"
DEFAULT_MD = ROOT / "reports/benchmark/manifests/safety-refusal-suite-20260616.md"
DEFAULT_QUEUE = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-suite-queue-20260616.json"
SSD_OUTPUT_ROOT = "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_queue_command(queue_path: Path) -> list[str]:
    failures: list[str] = []
    queue = load_json(queue_path)
    item = next((item for item in queue.get("items", []) if item.get("suite") == "safety-refusal"), None)
    if not item:
        return ["queue missing safety-refusal item"]
    command = str(item.get("local_command", ""))
    if "--suite reports/benchmark/manifests/safety-refusal-suite-20260616.json" not in command:
        failures.append("safety-refusal command must use --suite and the pinned manifest")
    if "--config" in command:
        failures.append("safety-refusal command must not use stale --config")
    if SSD_OUTPUT_ROOT not in command or item.get("output_root") != SSD_OUTPUT_ROOT:
        failures.append("safety-refusal command/output_root must be SSD-backed")
    if item.get("status") != "missing":
        failures.append("safety-refusal must remain missing until scored artifacts exist")
    return failures


def validate_manifest(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {display_path(path)}"]
    suite = load_json(path)
    if not isinstance(suite, list):
        return [f"{display_path(path)} must be a JSON array"]
    try:
        validate_suite(suite, path)
    except Exception as exc:  # noqa: BLE001
        failures.append(f"{display_path(path)} failed tool-call suite validation: {exc}")
        return failures
    categories = Counter(str(case.get("category")) for case in suite)
    if categories["invalid_tool_handling"] < 5:
        failures.append("safety/refusal suite must include at least five invalid/disallowed tool cases")
    for case in suite:
        if case.get("category") != "invalid_tool_handling":
            continue
        expected = case.get("expected", {})
        forbidden = expected.get("must_not_contain_any")
        if not isinstance(forbidden, list) or not forbidden:
            failures.append(f"{case.get('id')}: invalid/disallowed case must define forbidden markers")
        if expected.get("must_not_have_tool_calls") is not True:
            failures.append(f"{case.get('id')}: invalid/disallowed case must forbid tool calls")
    return failures


def validate_generated_files(created_at: str | None = None) -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        expected_json = tmpdir / "suite.json"
        expected_md = tmpdir / "suite.md"
        command = [
            sys.executable,
            "scripts/materialize_safety_refusal_suite.py",
            "--json-output",
            str(expected_json),
            "--markdown-output",
            str(expected_md),
        ]
        if created_at:
            command.extend(["--created-at", created_at])
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
        if DEFAULT_SUITE.read_text(encoding="utf-8") != expected_json.read_text(encoding="utf-8"):
            failures.append(f"{display_path(DEFAULT_SUITE)} is stale; regenerate it")
        if DEFAULT_MD.read_text(encoding="utf-8") != expected_md.read_text(encoding="utf-8"):
            failures.append(f"{display_path(DEFAULT_MD)} is stale; regenerate it")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MD)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--created-at", default="2026-06-16T00:00:00+00:00")
    args = parser.parse_args()

    failures: list[str] = []
    if not args.markdown.exists():
        failures.append(f"missing {display_path(args.markdown)}")
    failures.extend(validate_manifest(args.suite))
    failures.extend(validate_queue_command(args.queue))
    if not failures:
        failures.extend(validate_generated_files(args.created_at))
    if failures:
        print("not ready: safety/refusal suite")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: safety/refusal suite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
