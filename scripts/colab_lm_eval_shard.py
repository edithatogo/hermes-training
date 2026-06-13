#!/usr/bin/env python3
"""Launch or recover a Colab PEFT lm-eval shard with explicit artifacts."""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ADAPTER = Path("/Volumes/PortableSSD/hermes-evals/adapters/qwen3-v4-peft-conversion-20260613-clean.tar.gz")
DEFAULT_SCRIPT = ROOT / "scripts/colab_peft_lm_eval_selected.py"
DEFAULT_REMOTE_ADAPTER = "/content/qwen3-v4-peft-conversion-20260613.tar.gz"
DEFAULT_REMOTE_CONFIG = "/content/qwen3-v4-peft-lm-eval-config.json"
DEFAULT_OUTPUT_ROOT = Path("/Volumes/PortableSSD/hermes-evals/colab")


def load_config(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def command_plan(
    *,
    session: str,
    gpu: str,
    config: Path,
    adapter: Path,
    script: Path,
    exec_timeout_s: int,
) -> list[list[str]]:
    return [
        ["colab", "new", "-s", session, "--gpu", gpu],
        ["colab", "upload", "-s", session, str(adapter), DEFAULT_REMOTE_ADAPTER],
        ["colab", "upload", "-s", session, str(config), DEFAULT_REMOTE_CONFIG],
        ["colab", "exec", "-s", session, "--file", str(script), "--timeout", str(exec_timeout_s)],
    ]


def session_missing(status_text: str) -> bool:
    return "not found" in status_text.lower() or "session_not_found" in status_text.lower()


def run_command(
    command: list[str],
    log_path: Path | None,
    dry_run: bool,
    *,
    session: str | None = None,
    watchdog_s: float = 0.0,
) -> dict[str, Any]:
    started = datetime.now(UTC)
    if dry_run:
        return {
            "command": command,
            "quoted_command": shlex.join(command),
            "status": "planned",
            "started_at": started.isoformat(),
            "returncode": None,
            "log": str(log_path) if log_path else None,
        }
    if not log_path:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        return {
            "command": command,
            "quoted_command": shlex.join(command),
            "status": "ok" if result.returncode == 0 else "blocked",
            "started_at": started.isoformat(),
            "finished_at": datetime.now(UTC).isoformat(),
            "returncode": result.returncode,
            "log": None,
            "stdout_tail": result.stdout[-4000:],
            "stderr_tail": result.stderr[-4000:],
        }

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as handle:
        process = subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT, text=True)  # noqa: S603
        termination_reason = ""
        while process.poll() is None:
            if session and watchdog_s > 0:
                time.sleep(watchdog_s)
                status = subprocess.run(
                    ["colab", "status", "-s", session],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                status_text = f"{status.stdout}\n{status.stderr}"
                if session_missing(status_text):
                    termination_reason = "session-not-found"
                    process.kill()
                    process.wait()
                    break
            else:
                time.sleep(1)
        returncode = process.returncode
    return {
        "command": command,
        "quoted_command": shlex.join(command),
        "status": "ok" if returncode == 0 and not termination_reason else "blocked",
        "started_at": started.isoformat(),
        "finished_at": datetime.now(UTC).isoformat(),
        "returncode": returncode,
        "termination_reason": termination_reason,
        "log": str(log_path),
        "stdout_tail": "",
        "stderr_tail": "",
    }


def download_summary(session: str, remote_json: str, local_json: Path, dry_run: bool) -> dict[str, Any]:
    command = ["colab", "download", "-s", session, remote_json, str(local_json)]
    result = run_command(command, None, dry_run)
    if not dry_run and local_json.exists():
        try:
            data = json.loads(local_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            result["summary_error"] = f"JSONDecodeError: {exc}"
        else:
            result["summary_status"] = data.get("status")
            result["summary_checkpoint_phase"] = data.get("checkpoint_phase")
            result["summary_result_files"] = data.get("result_files")
    return result


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# Colab lm-eval Shard: {summary['session']}",
        "",
        f"Date: {summary['created_at']}",
        f"Mode: `{summary['mode']}`",
        f"Status: `{summary['status']}`",
        f"Config: `{summary['config']}`",
        f"Local output: `{summary['local_output']}`",
        "",
        "## Commands",
        "",
        "| Step | Status | Command | Log |",
        "|---|---|---|---|",
    ]
    for index, item in enumerate(summary.get("steps", []), 1):
        lines.append(
            f"| {index} | `{item['status']}` | `{item['quoted_command']}` | `{item.get('log') or ''}` |"
        )
    if summary.get("recovery"):
        recovery = summary["recovery"]
        lines.extend(
            [
                "",
                "## Recovery",
                "",
                f"- Summary status: `{recovery.get('summary_status', '')}`",
                f"- Checkpoint phase: `{recovery.get('summary_checkpoint_phase', '')}`",
                f"- Result files: `{recovery.get('summary_result_files', '')}`",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("launch", "recover"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--session")
    parser.add_argument("--gpu", default="T4")
    parser.add_argument("--adapter", type=Path, default=DEFAULT_ADAPTER)
    parser.add_argument("--script", type=Path, default=DEFAULT_SCRIPT)
    parser.add_argument("--exec-timeout-s", type=int, default=21600)
    parser.add_argument("--exec-watchdog-s", type=float, default=60.0)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    run_id = str(config.get("run_id") or args.config.stem)
    session = args.session or f"{run_id}-retry"
    local_output = args.output_root / session
    recovered = local_output / "recovered"
    recovered.mkdir(parents=True, exist_ok=True)
    report = args.report or Path("reports/colab") / f"{session}.md"
    remote_json = str(config.get("result_json") or f"/content/{run_id}.json")

    steps: list[dict[str, Any]] = []
    status = "planned" if args.dry_run else "ok"
    if args.mode == "launch":
        logs = ["colab-new.log", "upload-adapter.log", "upload-config.log", "colab-exec.log"]
        for command, log_name in zip(
            command_plan(
                session=session,
                gpu=args.gpu,
                config=args.config,
                adapter=args.adapter,
                script=args.script,
                exec_timeout_s=args.exec_timeout_s,
            ),
            logs,
            strict=True,
        ):
            watchdog_s = args.exec_watchdog_s if "exec" in command else 0.0
            step = run_command(command, local_output / log_name, args.dry_run, session=session, watchdog_s=watchdog_s)
            steps.append(step)
            if step["status"] == "blocked":
                status = "blocked"
                break

    recovery = download_summary(session, remote_json, recovered / "summary.json", args.dry_run)
    if recovery["status"] == "blocked" and not args.dry_run:
        status = "blocked"

    summary = {
        "created_at": datetime.now(UTC).isoformat(),
        "mode": args.mode,
        "status": status,
        "session": session,
        "config": str(args.config),
        "local_output": str(local_output),
        "remote_json": remote_json,
        "steps": steps,
        "recovery": recovery,
    }
    (local_output / "shard-wrapper-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if status in {"ok", "planned"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
