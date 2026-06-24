#!/usr/bin/env python3
"""Validate the Qwen3 v4 RULER ctx8192 runtime-blocker report."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-ruler-ctx8192-runtime-blocker-20260624.json"
REPORT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-ruler-ctx8192-runtime-blocker-20260624.md"


def main() -> int:
    failures: list[str] = []
    for path in (REPORT_JSON, REPORT_MD):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        return finish(failures)

    data = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    if data.get("status") != "blocked-runtime-generation-stall":
        failures.append("status must remain blocked-runtime-generation-stall")
    if int(data.get("context_length", 0)) != 8192:
        failures.append("context_length must be 8192")
    if int(data.get("limit", 0)) != 20:
        failures.append("limit must be 20")
    if int(data.get("terminated_after_seconds", 0)) < 300:
        failures.append("termination duration must show a real runtime stall")
    progress = data.get("observed_progress", {})
    required_progress = {
        "model_loaded": True,
        "synthetic_samples_generated": 500,
        "contexts_built": 20,
        "generate_until_started": True,
        "generate_until_completed": 0,
        "result_json_written": False,
    }
    for key, expected in required_progress.items():
        if progress.get(key) != expected:
            failures.append(f"observed_progress.{key} must be {expected!r}")
    if "No ctx8192 score was produced" not in str(data.get("blocker", "")):
        failures.append("blocker must explicitly state that no ctx8192 score was produced")
    if "only scored long-context evidence remains ctx4096" not in str(data.get("publication_boundary", "")):
        failures.append("publication boundary must keep ctx4096 as the only scored evidence")
    if "max_length=8192" not in str(data.get("command", "")):
        failures.append("command must record max_length=8192")

    md = REPORT_MD.read_text(encoding="utf-8")
    for needle in (
        "No ctx8192 score was produced.",
        "This is a runtime-blocker artifact, not a RULER score.",
        "ctx4096 `niah_single_1 = 1.000` over 500 samples",
    ):
        if needle not in md:
            failures.append(f"markdown report missing {needle!r}")
    return finish(failures)


def finish(failures: list[str]) -> int:
    if failures:
        print("not ready: RULER ctx8192 runtime blocker")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: RULER ctx8192 runtime blocker")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
