#!/usr/bin/env python3
"""Run a Colab script on the first available accelerator in a priority list."""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


DEFAULT_ACCELERATORS = "gpu:T4,gpu:L4,gpu:A100,tpu:v5e1"


@dataclass(frozen=True)
class Accelerator:
    kind: str
    name: str

    @property
    def colab_args(self) -> list[str]:
        return [f"--{self.kind}", self.name]

    @property
    def label(self) -> str:
        return f"{self.kind}-{self.name}".replace("/", "-")


def resolve_storage_root() -> Path:
    if os.environ.get("HERMES_STORAGE_ROOT"):
        return Path(os.environ["HERMES_STORAGE_ROOT"])
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD")
    return Path.cwd() / ".local-storage"


def parse_accelerators(raw: str, allow_tpu: bool) -> list[Accelerator]:
    accelerators: list[Accelerator] = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise ValueError(f"accelerator must use kind:name format, got {item!r}")
        kind, name = [part.strip() for part in item.split(":", 1)]
        if kind not in {"gpu", "tpu"}:
            raise ValueError(f"unsupported accelerator kind {kind!r}")
        if kind == "tpu" and not allow_tpu:
            continue
        accelerators.append(Accelerator(kind=kind, name=name))
    if not accelerators:
        raise ValueError("no accelerators remain after applying TPU policy")
    return accelerators


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-") or "colab-run"


def run_colab(
    accelerator: Accelerator,
    script: Path,
    script_args: list[str],
    timeout_s: float,
    output_dir: Path,
    dry_run: bool,
    attempt_index: int,
) -> dict[str, Any]:
    command = ["colab", "run", *accelerator.colab_args, "--timeout", str(timeout_s), str(script), *script_args]
    log_suffix = f"{accelerator.label}.log" if attempt_index == 1 else f"{accelerator.label}-attempt{attempt_index}.log"
    log_path = output_dir / log_suffix
    started = time.time()
    if dry_run:
        return {
            "accelerator": accelerator.__dict__,
            "status": "planned",
            "attempt_index": attempt_index,
            "command": command,
            "quoted_command": shlex.join(command),
            "log": str(log_path),
            "duration_s": 0.0,
        }
    with log_path.open("w", encoding="utf-8") as handle:
        process = subprocess.run(command, check=False, stdout=handle, stderr=subprocess.STDOUT, text=True)
    duration = time.time() - started
    log_text = log_path.read_text(encoding="utf-8", errors="replace")
    return {
        "accelerator": accelerator.__dict__,
        "status": "scored" if process.returncode == 0 else "blocked",
        "attempt_index": attempt_index,
        "returncode": process.returncode,
        "command": command,
        "quoted_command": shlex.join(command),
        "log": str(log_path),
        "duration_s": duration,
        "observed": extract_observed_runtime(log_text),
        "tail": "\n".join(log_text.splitlines()[-40:]),
    }


def extract_observed_runtime(log_text: str) -> dict[str, str]:
    observed: dict[str, str] = {}
    for pattern, key in [
        (r'"cuda_device_name":\s*"([^"]+)"', "cuda_device_name"),
        (r'"cuda_available":\s*(true|false)', "cuda_available"),
        (r'"xla_device":\s*"([^"]+)"', "xla_device"),
        (r'"torch_xla_available":\s*(true|false)', "torch_xla_available"),
        (r'"backend":\s*"([^"]+)"', "training_backend"),
        (r'"device_name":\s*"([^"]+)"', "training_device_name"),
    ]:
        match = re.search(pattern, log_text)
        if match:
            observed[key] = match.group(1)
    return observed


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# Colab Dispatch: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        f"Status: `{summary['status']}`",
        f"Script: `{summary['script']}`",
        f"Output: `{summary['output_dir']}`",
        "",
        "## Attempts",
        "",
        "| Accelerator | Status | Duration | Log | Observed |",
        "|---|---|---:|---|---|",
    ]
    for attempt in summary["attempts"]:
        accel = attempt["accelerator"]
        observed = ", ".join(f"{key}={value}" for key, value in attempt.get("observed", {}).items()) or "none"
        lines.append(
            f"| `{accel['kind']}:{accel['name']}` | `{attempt['status']}` | {attempt['duration_s']:.3f}s | `{attempt['log']}` | {observed} |"
        )
    lines.extend(["", "## Decision", "", summary["decision"], ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accelerators", default=DEFAULT_ACCELERATORS)
    parser.add_argument("--allow-tpu", action="store_true", help="Allow TPU candidates in the accelerator list.")
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--retries", type=int, default=0, help="Retry each accelerator this many times after the first failed attempt.")
    parser.add_argument("--retry-delay-s", type=float, default=5.0)
    parser.add_argument("--run-id", default=f"colab-dispatch-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("script", type=Path)
    parser.add_argument("script_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    accelerators = parse_accelerators(args.accelerators, allow_tpu=args.allow_tpu)
    output_dir = args.output_dir or resolve_storage_root() / "hermes-evals" / "colab" / slugify(args.run_id)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.report or Path("reports/colab") / f"{slugify(args.run_id)}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    attempts: list[dict[str, Any]] = []
    status = "blocked"
    for accelerator in accelerators:
        for attempt_index in range(1, args.retries + 2):
            attempt = run_colab(
                accelerator,
                args.script,
                args.script_args,
                args.timeout,
                output_dir,
                args.dry_run,
                attempt_index,
            )
            attempts.append(attempt)
            if attempt["status"] in {"planned", "scored"}:
                status = attempt["status"]
                break
            if attempt_index <= args.retries and args.retry_delay_s > 0 and not args.dry_run:
                time.sleep(args.retry_delay_s)
        if status in {"planned", "scored"}:
            if not args.dry_run:
                break

    summary = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "status": status,
        "script": str(args.script),
        "script_args": args.script_args,
        "accelerators_requested": [accel.__dict__ for accel in accelerators],
        "output_dir": str(output_dir),
        "report": str(report_path),
        "attempts": attempts,
        "decision": (
            "Dry run only; no Colab runtime was created."
            if args.dry_run
            else "First available accelerator completed successfully."
            if status == "scored"
            else "No requested accelerator completed successfully."
        ),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if status in {"planned", "scored"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
