#!/usr/bin/env python3
"""Validate the Qwen3 v4 PEFT scorecard backend selection report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHECKLIST = ROOT / "reports/cloud/backend-unblock-checklist-20260613.json"
DEFAULT_JSON = ROOT / "reports/cloud/qwen3-v4-peft-scorecard-backend-selection-20260614.json"
DEFAULT_MD = ROOT / "reports/cloud/qwen3-v4-peft-scorecard-backend-selection-20260614.md"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def validate_semantics(path: Path) -> list[str]:
    failures: list[str] = []
    data = load_json(path)
    if data.get("status") != "blocked-pending-operator-gates":
        failures.append("backend selection must remain blocked pending operator gates")
    if data.get("execute") is not False:
        failures.append("backend selection must not enable execution")
    if data.get("promotion_allowed") is not False:
        failures.append("backend selection must not allow benchmark promotion")
    if data.get("selected_backend") != "kaggle":
        failures.append("current selected backend must be kaggle, the only prepared run-approval route")
    gates = set(data.get("required_before_execution", []))
    for gate in {
        "explicit run approval",
        "cost or zero-cost policy confirmation",
        "artifact recovery plan",
    }:
        if gate not in gates:
            failures.append(f"missing execution gate: {gate}")
    ranked = data.get("ranked_backends", [])
    if not isinstance(ranked, list) or not ranked:
        failures.append("backend selection must include ranked backends")
    else:
        scores = [int(row.get("score", 0)) for row in ranked if isinstance(row, dict)]
        if scores != sorted(scores, reverse=True):
            failures.append("ranked backends must be sorted by descending score")
        colab = next((row for row in ranked if isinstance(row, dict) and row.get("backend") == "colab"), None)
        if not colab or int(colab.get("score", 0)) >= int(ranked[0].get("score", 0)):
            failures.append("colab must not be selected while pruning/keepalive blockers remain")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    parser.add_argument("--selection-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--selection-md", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    failures: list[str] = []
    for path in (args.checklist, args.selection_json, args.selection_md):
        if not path.exists():
            failures.append(f"missing {display_path(path)}")
    if not failures:
        failures.extend(validate_semantics(args.selection_json))
    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected_json = tmpdir / "selection.json"
            expected_md = tmpdir / "selection.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/select_scorecard_backend.py"),
                    "--checklist",
                    str(args.checklist),
                    "--json-output",
                    str(expected_json),
                    "--markdown-output",
                    str(expected_md),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode:
                failures.append(f"generator failed: {result.stdout.strip()} {result.stderr.strip()}".strip())
            elif expected_json.read_text() != args.selection_json.read_text():
                failures.append(f"{display_path(args.selection_json)} is stale; regenerate it")
            elif expected_md.read_text() != args.selection_md.read_text():
                failures.append(f"{display_path(args.selection_md)} is stale; regenerate it")
    if failures:
        print("not ready: scorecard backend selection")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: scorecard backend selection is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
