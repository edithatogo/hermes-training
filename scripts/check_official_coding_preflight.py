#!/usr/bin/env python3
"""Preflight the official coding candidate slice without executing tests."""
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
DEFAULT_JSON_OUTPUT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-coding-preflight-20260616.json"
DEFAULT_MD_OUTPUT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-coding-preflight-20260616.md"
BENCHMARK_PYTHON = Path("/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python")
EVALPLUS_CLI = Path("/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/evalplus.evaluate")
EXPECTED_SUITE = "official-coding"
EXPECTED_RUN_ID = "qwen3-v4-peft-official-coding-20260616"
EXPECTED_HUMANEVAL_ROWS = 164


@dataclass(frozen=True)
class JsonlStatus:
    path: str
    present: bool
    rows: int
    valid_jsonl: bool
    error: str


def load_queue(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_coding_item(queue: dict[str, Any]) -> dict[str, Any]:
    for item in queue.get("items", []):
        if isinstance(item, dict) and item.get("suite") == EXPECTED_SUITE:
            return item
    raise ValueError(f"{EXPECTED_SUITE} not found in official candidate suite queue")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def module_present(module: str) -> bool:
    if not BENCHMARK_PYTHON.exists():
        return False
    code = f"import importlib.util, sys; sys.exit(0 if importlib.util.find_spec({module!r}) else 1)"
    result = subprocess.run([str(BENCHMARK_PYTHON), "-c", code], capture_output=True, text=True, timeout=20)
    return result.returncode == 0


def command_status(command: Path) -> dict[str, Any]:
    if not command.exists():
        return {"path": str(command), "present": False, "executable": False, "help_output": ""}
    executable = os.access(command, os.X_OK)
    help_output = ""
    if executable:
        result = subprocess.run([str(command), "--help"], capture_output=True, text=True, timeout=20)
        for line in (result.stdout or result.stderr).splitlines():
            if line.strip():
                help_output = line.strip()
                break
    return {"path": str(command), "present": True, "executable": executable, "help_output": help_output}


def generated_jsonl_status(path: Path) -> JsonlStatus:
    if not path.exists():
        return JsonlStatus(path=str(path), present=False, rows=0, valid_jsonl=False, error="generated solutions JSONL is missing")
    rows = 0
    try:
        with path.open(encoding="utf-8") as handle:
            for rows, line in enumerate(handle, 1):
                data = json.loads(line)
                if not isinstance(data, dict):
                    return JsonlStatus(path=str(path), present=True, rows=rows, valid_jsonl=False, error=f"line {rows} is not an object")
    except Exception as exc:  # noqa: BLE001
        return JsonlStatus(path=str(path), present=True, rows=rows, valid_jsonl=False, error=f"{type(exc).__name__}: {exc}")
    if rows != EXPECTED_HUMANEVAL_ROWS:
        return JsonlStatus(
            path=str(path),
            present=True,
            rows=rows,
            valid_jsonl=False,
            error=f"expected {EXPECTED_HUMANEVAL_ROWS} HumanEval rows, found {rows}",
        )
    return JsonlStatus(path=str(path), present=True, rows=rows, valid_jsonl=True, error="")


def parse_samples_path(command: str) -> Path:
    parts = command.split()
    if "--samples" not in parts:
        return Path("")
    index = parts.index("--samples")
    if index + 1 >= len(parts):
        return Path("")
    return Path(parts[index + 1])


def is_ssd_backed(path: str) -> bool:
    return path.startswith("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/")


def build_report(queue_path: Path = DEFAULT_QUEUE, created_at: str | None = None) -> dict[str, Any]:
    queue = load_queue(queue_path)
    item = find_coding_item(queue)
    command = str(item.get("local_command", ""))
    output_root = str(item.get("output_root", ""))
    samples_path = parse_samples_path(command)
    samples = generated_jsonl_status(samples_path)
    evalplus = command_status(EVALPLUS_CLI)
    checks = {
        "queue_item_present": True,
        "suite_status_missing": item.get("status") == "missing",
        "run_id_matches": item.get("run_id") == EXPECTED_RUN_ID,
        "output_root_ssd_backed": is_ssd_backed(output_root),
        "command_uses_evalplus_module": f"{BENCHMARK_PYTHON} -m evalplus.evaluate" in command,
        "command_uses_positional_humaneval": "evalplus.evaluate humaneval" in command,
        "command_uses_samples": "--samples" in command and str(samples_path),
        "command_omits_stale_model_flag": "--model" not in command and "--dataset" not in command,
        "evalplus_cli_executable": bool(evalplus["present"] and evalplus["executable"]),
        "evalplus_module_present": module_present("evalplus"),
        "human_eval_module_present": module_present("human_eval"),
        "generated_solutions_present": samples.present and samples.valid_jsonl,
    }
    blockers: list[str] = []
    for name, passed in checks.items():
        if not passed and name != "generated_solutions_present":
            blockers.append(name.replace("_", " "))
    if not checks["generated_solutions_present"]:
        blockers.append(samples.error or "generated solutions JSONL is not ready")
    status = "ready-to-evaluate" if not blockers else "blocked-coding-preflight"
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
        "samples": {
            "path": samples.path,
            "present": samples.present,
            "rows": samples.rows,
            "valid_jsonl": samples.valid_jsonl,
            "error": samples.error,
        },
        "evalplus_cli": evalplus,
        "checks": checks,
        "blockers": blockers,
        "local_command": command,
        "publication_boundary": item.get("publication_boundary", ""),
        "decision": (
            "Generate solutions first, then run EvalPlus with execution enabled; "
            "this preflight is not scored benchmark evidence."
        ),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 v4 Official Coding Preflight",
        "",
        f"Date: {report['created_at']}",
        f"Status: `{report['status']}`",
        f"Suite: `{report['suite']}`",
        f"Run ID: `{report['run_id']}`",
        f"Candidate: `{report['candidate']}`",
        f"Adapter: `{report['adapter']}`",
        f"Output root: `{report['output_root']}`",
        "",
        "This report is a launch gate for HumanEval/EvalPlus execution. It does not contain pass@k scores.",
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
            "## Generated Solutions",
            "",
            f"- Path: `{report['samples']['path'] or '(not parsed)'}`",
            f"- Present: `{str(report['samples']['present']).lower()}`",
            f"- Rows: `{report['samples']['rows']}`",
            f"- Valid JSONL: `{str(report['samples']['valid_jsonl']).lower()}`",
            f"- Error: {report['samples']['error'] or 'none'}",
            "",
            "## EvalPlus",
            "",
            f"- CLI: `{report['evalplus_cli']['path']}`",
            f"- Present: `{str(report['evalplus_cli']['present']).lower()}`",
            f"- Executable: `{str(report['evalplus_cli']['executable']).lower()}`",
            f"- Help line: `{report['evalplus_cli']['help_output']}`",
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
