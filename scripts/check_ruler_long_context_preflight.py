#!/usr/bin/env python3
"""Preflight the RULER long-context candidate slice without running it."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-suite-queue-20260616.json"
DEFAULT_JSON_OUTPUT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-ruler-long-context-preflight-20260616.json"
DEFAULT_MD_OUTPUT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-ruler-long-context-preflight-20260616.md"
BENCHMARK_PYTHON = Path("/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python")
EXPECTED_SUITE = "ruler-long-context"
EXPECTED_RUN_ID = "qwen3-v4-peft-ruler-long-context-20260616"
INITIAL_CONTEXT = 4096
CONTEXT_LADDER = (4096, 8192, 16384)


@dataclass(frozen=True)
class ModuleStatus:
    name: str
    present: bool
    detail: str


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def find_ruler_item(queue: dict[str, Any]) -> dict[str, Any]:
    for item in queue.get("items", []):
        if isinstance(item, dict) and item.get("suite") == EXPECTED_SUITE:
            return item
    raise ValueError(f"{EXPECTED_SUITE} not found in official candidate suite queue")


def module_status(module: str) -> ModuleStatus:
    if not BENCHMARK_PYTHON.exists():
        return ModuleStatus(module, False, f"{BENCHMARK_PYTHON} does not exist")
    code = (
        "import importlib.util, json; "
        f"spec=importlib.util.find_spec({module!r}); "
        "print(json.dumps({'present': bool(spec), 'origin': getattr(spec, 'origin', '') if spec else ''}))"
    )
    result = subprocess.run([str(BENCHMARK_PYTHON), "-c", code], capture_output=True, text=True, timeout=20)
    if result.returncode:
        return ModuleStatus(module, False, (result.stderr or result.stdout).strip())
    payload = json.loads(result.stdout)
    return ModuleStatus(module, bool(payload.get("present")), str(payload.get("origin") or ""))


def is_ssd_backed(path: str) -> bool:
    return path.startswith("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/")


def build_report(queue_path: Path = DEFAULT_QUEUE, created_at: str | None = None) -> dict[str, Any]:
    queue = load_json(queue_path)
    item = find_ruler_item(queue)
    command = str(item.get("local_command", ""))
    output_root = str(item.get("output_root", ""))
    ruler = module_status("lm_eval.tasks.ruler")
    checks = {
        "queue_item_present": True,
        "suite_status_missing": item.get("status") == "missing",
        "run_id_matches": item.get("run_id") == EXPECTED_RUN_ID,
        "output_root_ssd_backed": is_ssd_backed(output_root),
        "command_uses_lm_eval": "lm_eval run --model hf" in command,
        "command_uses_ruler_task": "--tasks niah_single_1" in command,
        "command_uses_mps_device": "--device mps" in command,
        "command_sets_model_max_length": "max_length=4096" in command,
        "command_sets_ruler_metadata": "max_seq_lengths" in command and "4096" in command,
        "command_uses_initial_context": "ctx4096" in command,
        "command_omits_context_placeholder": "<context>" not in command,
        "command_writes_ctx4096": "ctx4096" in command,
        "benchmark_python_present": BENCHMARK_PYTHON.exists() and os.access(BENCHMARK_PYTHON, os.X_OK),
        "lm_eval_ruler_tasks_present": ruler.present,
    }
    blockers: list[str] = []
    for name, passed in checks.items():
        if not passed and name != "lm_eval_ruler_tasks_present":
            blockers.append(name.replace("_", " "))
    if not ruler.present:
        blockers.append("lm_eval RULER tasks are not installed in the SSD benchmark environment")
    status = "ready-to-run" if not blockers else "blocked-ruler-preflight"
    return {
        "created_at": created_at or datetime.now(UTC).isoformat(),
        "status": status,
        "suite": EXPECTED_SUITE,
        "run_id": EXPECTED_RUN_ID,
        "candidate": queue.get("candidate"),
        "base_model": queue.get("base_model"),
        "adapter": queue.get("adapter"),
        "queue_path": display_path(queue_path),
        "output_root": output_root,
        "context_decision": {
            "initial_max_seq_length": INITIAL_CONTEXT,
            "ladder": list(CONTEXT_LADDER),
            "task": "niah_single_1",
            "reason": "Start with a bounded needle/retrieval smoke before scaling context length.",
        },
        "modules": {
            "lm_eval.tasks.ruler": {"present": ruler.present, "detail": ruler.detail},
        },
        "checks": checks,
        "blockers": blockers,
        "local_command": command,
        "publication_boundary": item.get("publication_boundary", ""),
        "decision": (
            "Use the installed lm_eval RULER task path before running the ctx4096 stage; "
            "this preflight is not scored benchmark evidence."
        ),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 v4 RULER Long-Context Preflight",
        "",
        f"Date: {report['created_at']}",
        f"Status: `{report['status']}`",
        f"Suite: `{report['suite']}`",
        f"Run ID: `{report['run_id']}`",
        f"Candidate: `{report['candidate']}`",
        f"Adapter: `{report['adapter']}`",
        f"Output root: `{report['output_root']}`",
        "",
        "This report is a launch gate for the RULER long-context slice. It does not contain RULER scores.",
        "",
        "## Context Decision",
        "",
        f"- Initial context: `{report['context_decision']['initial_max_seq_length']}`",
        f"- Context ladder: `{report['context_decision']['ladder']}`",
        f"- Task: `{report['context_decision']['task']}`",
        f"- Reason: {report['context_decision']['reason']}",
        "",
        "## Checks",
        "",
        "| Check | Pass |",
        "|---|---:|",
    ]
    for name, passed in report["checks"].items():
        lines.append(f"| `{name}` | `{str(bool(passed)).lower()}` |")
    lines.extend(
        [
            "",
            "## Runtime",
            "",
            f"- lm_eval RULER tasks present: `{str(report['modules']['lm_eval.tasks.ruler']['present']).lower()}`",
            f"- Detail: `{report['modules']['lm_eval.tasks.ruler']['detail']}`",
            "",
            "## Blockers",
            "",
        ]
    )
    if report["blockers"]:
        for blocker in report["blockers"]:
            lines.append(f"- {blocker}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Command",
            "",
            "```bash",
            report["local_command"],
            "```",
            "",
            "## Decision",
            "",
            report["decision"],
            f"Publication boundary: {report['publication_boundary']}",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_MD_OUTPUT)
    parser.add_argument("--created-at", help="Override timestamp for deterministic regeneration checks.")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    report = build_report(queue_path=args.queue, created_at=args.created_at)
    if not args.no_write:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        args.output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"status": report["status"], "blockers": report["blockers"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
