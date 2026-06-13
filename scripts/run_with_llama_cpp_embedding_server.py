#!/usr/bin/env python3
"""Run a command while a llama.cpp embedding server is kept alive."""
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

import requests


def resolve_default_output_root() -> Path:
    env_eval_root = os.environ.get("HERMES_EVAL_ROOT")
    if env_eval_root:
        return Path(env_eval_root)
    storage_root = os.environ.get("HERMES_STORAGE_ROOT")
    if storage_root:
        return Path(storage_root) / "hermes-evals"
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD") / "hermes-evals"
    return Path.cwd() / ".local-storage" / "hermes-evals"


def wait_for_server(base_url: str, process: subprocess.Popen[bytes], timeout_s: float) -> dict[str, object]:
    deadline = time.time() + timeout_s
    last_error = ""
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"llama-server exited before readiness with code {process.returncode}: {last_error}")
        try:
            response = requests.get(base_url.rstrip("/") + "/models", timeout=2)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                return data
            return {"raw": data}
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
            time.sleep(1)
    raise TimeoutError(f"llama-server did not become ready within {timeout_s:.1f}s: {last_error}")


def terminate_process(process: subprocess.Popen[bytes], timeout_s: float = 10.0) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=timeout_s)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--llama-server-bin", type=Path, default=Path("/opt/homebrew/bin/llama-server"))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8095)
    parser.add_argument("--ctx-size", type=int, default=512)
    parser.add_argument("--pooling", default="mean")
    parser.add_argument("--embd-normalize", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=512)
    parser.add_argument("--ubatch-size", type=int, default=512)
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--startup-timeout-s", type=float, default=60.0)
    parser.add_argument("--run-id", default=f"llama-cpp-embedding-server-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--log-dir", type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to run after `--`.")
    args = parser.parse_args()

    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise ValueError("provide a command after --")
    if not args.model_path.exists():
        raise FileNotFoundError(args.model_path)
    if not args.llama_server_bin.exists():
        raise FileNotFoundError(args.llama_server_bin)

    base_url = f"http://{args.host}:{args.port}/v1"
    log_dir = args.log_dir or (resolve_default_output_root() / "server-logs" / args.run_id)
    log_dir.mkdir(parents=True, exist_ok=True)
    server_log_path = log_dir / "llama-server.log"
    command_log_path = log_dir / "command.log"
    manifest_path = log_dir / "manifest.json"

    server_cmd = [
        str(args.llama_server_bin),
        "-m",
        str(args.model_path),
        "--embedding",
        "--pooling",
        args.pooling,
        "--embd-normalize",
        str(args.embd_normalize),
        "--ctx-size",
        str(args.ctx_size),
        "--batch-size",
        str(args.batch_size),
        "--ubatch-size",
        str(args.ubatch_size),
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--parallel",
        str(args.parallel),
        "--cont-batching",
    ]
    manifest = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "base_url": base_url,
        "server_command": server_cmd,
        "command": command,
        "server_log": str(server_log_path),
        "command_log": str(command_log_path),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"status": "starting-server", "base_url": base_url, "log_dir": str(log_dir)}, indent=2))
    with server_log_path.open("wb") as server_log:
        server = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=server_log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        try:
            models = wait_for_server(base_url, server, args.startup_timeout_s)
            print(json.dumps({"status": "server-ready", "models": models.get("data", [])[:1]}, indent=2))
            env = os.environ.copy()
            env["LLAMA_CPP_EMBEDDING_BASE_URL"] = base_url
            started = time.time()
            with command_log_path.open("wb") as command_log:
                child = subprocess.run(command, stdout=command_log, stderr=subprocess.STDOUT, env=env, check=False)
            elapsed_s = time.time() - started
            server_returncode = server.poll()
            result = {
                "status": "passed" if child.returncode == 0 and server_returncode is None else "failed",
                "command_returncode": child.returncode,
                "server_returncode": server_returncode,
                "elapsed_s": round(elapsed_s, 3),
                "base_url": base_url,
                "log_dir": str(log_dir),
            }
            print(json.dumps(result, indent=2))
            return child.returncode if child.returncode != 0 else 0 if server_returncode is None else 1
        finally:
            if server.poll() is None:
                try:
                    os.killpg(server.pid, signal.SIGTERM)
                    server.wait(timeout=10)
                except Exception:  # noqa: BLE001
                    terminate_process(server)


if __name__ == "__main__":
    raise SystemExit(main())
