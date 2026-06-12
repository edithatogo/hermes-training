#!/usr/bin/env python3
"""Run the opt-in ColBERT mem0 read stack smoke with service lifecycle control."""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen


DEFAULT_QUERIES = [
    "What is the active mem0 Qdrant collection?",
    "Which embedding model is configured for local mem0?",
    "Which extraction model is currently configured for local mem0?",
]


def resolve_storage_root() -> Path:
    env_root = os.environ.get("HERMES_STORAGE_ROOT")
    if env_root:
        return Path(env_root)
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD")
    return Path.cwd() / ".local-storage"


def merged_runtime_env() -> dict[str, str]:
    env = os.environ.copy()
    storage_root = resolve_storage_root()
    env.setdefault("HERMES_STORAGE_ROOT", str(storage_root))
    env.setdefault("HF_HOME", str(storage_root / "huggingface"))
    env.setdefault("HF_HUB_CACHE", str(storage_root / "huggingface" / "hub"))
    env.setdefault("HF_HUB_DISABLE_XET", "1")
    env.setdefault("HF_DATASETS_CACHE", str(storage_root / "huggingface" / "datasets"))
    env.setdefault("TRANSFORMERS_CACHE", str(storage_root / "huggingface" / "transformers"))
    env.setdefault("XDG_CACHE_HOME", str(storage_root / "cache"))
    env.setdefault("PIP_CACHE_DIR", str(storage_root / "pip-cache"))
    env.setdefault("TORCH_HOME", str(storage_root / "torch"))
    env.setdefault("HERMES_EVAL_ROOT", str(storage_root / "hermes-evals"))
    env.setdefault("HERMES_EXPORT_ROOT", str(storage_root / "hermes-exports"))
    env.setdefault("TMPDIR", str(storage_root / "tmp"))
    for key in (
        "HF_HUB_CACHE",
        "HF_DATASETS_CACHE",
        "TRANSFORMERS_CACHE",
        "XDG_CACHE_HOME",
        "PIP_CACHE_DIR",
        "TORCH_HOME",
        "HERMES_EVAL_ROOT",
        "HERMES_EXPORT_ROOT",
        "TMPDIR",
    ):
        Path(env[key]).mkdir(parents=True, exist_ok=True)
    return env


def read_health(base_url: str, timeout_s: float) -> dict[str, Any]:
    with urlopen(base_url.rstrip("/") + "/health", timeout=timeout_s) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("health endpoint returned non-object JSON")
    return payload


def wait_for_health(base_url: str, startup_timeout_s: float, poll_interval_s: float) -> dict[str, Any]:
    deadline = time.time() + startup_timeout_s
    last_error = ""
    while time.time() < deadline:
        try:
            health = read_health(base_url, timeout_s=min(5.0, poll_interval_s))
        except (OSError, URLError, json.JSONDecodeError, RuntimeError) as exc:
            last_error = str(exc)
            time.sleep(poll_interval_s)
            continue
        if health.get("ok") is True:
            return health
        last_error = f"health returned ok={health.get('ok')!r}"
        time.sleep(poll_interval_s)
    raise TimeoutError(f"ColBERT service did not become healthy within {startup_timeout_s:.1f}s: {last_error}")


def stop_process(process: subprocess.Popen[str], timeout_s: float = 20.0) -> None:
    if process.poll() is not None:
        return
    process.send_signal(signal.SIGINT)
    try:
        process.wait(timeout=timeout_s)
        return
    except subprocess.TimeoutExpired:
        process.terminate()
    try:
        process.wait(timeout=10.0)
        return
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=10.0)


def wait_until_down(base_url: str, timeout_s: float = 30.0, poll_interval_s: float = 1.0) -> None:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            read_health(base_url, timeout_s=min(3.0, poll_interval_s))
        except (OSError, URLError, json.JSONDecodeError, RuntimeError):
            return
        time.sleep(poll_interval_s)
    raise TimeoutError(f"ColBERT service still responded after {timeout_s:.1f}s")


def run_probe(args: argparse.Namespace, run_id: str, queries: list[str], extra_flags: list[str]) -> dict[str, Any]:
    command = [
        sys.executable,
        str(Path(__file__).resolve().parent / "run_mem0_read_latency_probe.py"),
        "--mode",
        "colbert",
        "--iterations",
        str(args.iterations),
        "--run-id",
        run_id,
        "--timeout-s",
        str(args.mem0_timeout_s),
        "--read-wall-timeout-s",
        str(args.read_wall_timeout_s),
        "--retriever-service-url",
        args.service_url,
        "--retriever-timeout-s",
        str(args.retriever_timeout_s),
        "--retriever-top-k",
        str(args.retriever_top_k),
        "--subprocess-read",
        "--cache-ttl-s",
        "0",
        *extra_flags,
    ]
    for query in queries:
        command.extend(["--query", query])
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        env=merged_runtime_env(),
        timeout=args.probe_wall_timeout_s,
    )
    summary_path = resolve_storage_root() / "hermes-evals" / "mem0-read-latency" / run_id / "summary.json"
    try:
        return json.loads(summary_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"probe completed but summary could not be read: {summary_path}\nstderr={completed.stderr[-1000:]}") from exc


def render_report(payload: dict[str, Any]) -> str:
    service_up = payload["service_up_summary"]
    service_down = payload["service_down_summary"]
    health = payload["service_health"]
    return "\n".join(
        [
            f"# ColBERT Read Stack Smoke - {payload['created_at'][:10]}",
            "",
            "## Scope",
            "",
            "This smoke controls the local `LiquidAI/LFM2-ColBERT-350M` service lifecycle,",
            "runs the opt-in `mem0_read.py --mode colbert` wrapper while the service is",
            "healthy, then stops the service and verifies `--fallback-to-vector` behavior.",
            "",
            "## Service",
            "",
            f"- URL: `{payload['service_url']}`",
            f"- Model: `{health.get('model_id', '')}`",
            f"- Device: `{health.get('device', '')}`",
            f"- Local files only: `{health.get('local_files_only', '')}`",
            "",
            "## Service-Up Probe",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Success count | {service_up['success_count']} |",
            f"| Fallback count | {service_up['fallback_count']} |",
            f"| Multi-result count | {service_up['multi_result_count']} |",
            f"| Singleton count | {service_up['singleton_count']} |",
            f"| Empty count | {service_up['empty_count']} |",
            f"| Total latency p50 | {service_up['total_latency_p50_s']:.3f}s |",
            f"| mem0 search latency p50 | {service_up['mem0_search_latency_p50_s']:.3f}s |",
            f"| Retriever latency p50 | {service_up['rerank_latency_p50_s']:.3f}s |",
            "",
            f"Raw output: `{service_up['output_dir']}`",
            "",
            "## Service-Down Fallback Probe",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Success count | {service_down['success_count']} |",
            f"| Fallback count | {service_down['fallback_count']} |",
            f"| Total latency p50 | {service_down['total_latency_p50_s']:.3f}s |",
            f"| mem0 search latency p50 | {service_down['mem0_search_latency_p50_s']:.3f}s |",
            "",
            f"Raw output: `{service_down['output_dir']}`",
            "",
            "## Decision Use",
            "",
            "Use this report to decide whether the live ColBERT path has enough",
            "multi-candidate coverage and service lifecycle proof to become the default",
            "Hermes mem0 read path. If the service-up probe has only singleton results,",
            "the stack remains opt-in even when fallback is healthy.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--service-url", default="http://127.0.0.1:8765")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--model", default="LiquidAI/LFM2-ColBERT-350M")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--startup-timeout-s", type=float, default=180.0)
    parser.add_argument("--poll-interval-s", type=float, default=2.0)
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--query", action="append", default=[])
    parser.add_argument("--mem0-timeout-s", type=float, default=90.0)
    parser.add_argument("--read-wall-timeout-s", type=float, default=150.0)
    parser.add_argument("--retriever-timeout-s", type=float, default=120.0)
    parser.add_argument("--retriever-top-k", type=int, default=8)
    parser.add_argument("--probe-wall-timeout-s", type=float, default=600.0)
    parser.add_argument("--run-id-prefix", default=f"mem0-colbert-stack-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--report-path", type=Path)
    args = parser.parse_args()

    queries = args.query or DEFAULT_QUERIES
    service_command = [
        sys.executable,
        str(Path(__file__).resolve().parent / "lfm2_colbert_service.py"),
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--model",
        args.model,
        "--device",
        args.device,
        "--quiet",
    ]
    if args.local_files_only:
        service_command.append("--local-files-only")

    log_root = resolve_storage_root() / "hermes-evals" / "service-logs"
    log_root.mkdir(parents=True, exist_ok=True)
    service_log_path = log_root / f"{args.run_id_prefix}-lfm2-colbert-service.log"
    with service_log_path.open("w", encoding="utf-8") as service_log:
        service = subprocess.Popen(
            service_command,
            stdout=service_log,
            stderr=subprocess.STDOUT,
            text=True,
            env=merged_runtime_env(),
        )
        try:
            health = wait_for_health(args.service_url, args.startup_timeout_s, args.poll_interval_s)
            service_up_summary = run_probe(args, f"{args.run_id_prefix}-service-up", queries, ["--fallback-to-vector"])
        finally:
            stop_process(service)
    wait_until_down(args.service_url)

    # Confirm the fallback path after stopping the service.
    service_down_summary = run_probe(
        args,
        f"{args.run_id_prefix}-service-down-fallback",
        queries[:1],
        ["--fallback-to-vector"],
    )
    payload = {
        "created_at": datetime.now(UTC).isoformat(),
        "service_url": args.service_url,
        "service_log_path": str(service_log_path),
        "service_health": health,
        "service_up_summary": service_up_summary,
        "service_down_summary": service_down_summary,
    }
    report_path = args.report_path or (
        Path("reports/benchmark/mem0") / f"{args.run_id_prefix}-read-stack-smoke.md"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(payload), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"report: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
