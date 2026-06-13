#!/usr/bin/env python3
"""Run a command behind a restarting llama.cpp embedding proxy."""
from __future__ import annotations

import argparse
import json
import os
import signal
import site
import subprocess
import sys
import threading
import time
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import requests

try:
    from run_with_llama_cpp_embedding_server import resolve_default_output_root, terminate_process, wait_for_server
except ModuleNotFoundError:
    from scripts.run_with_llama_cpp_embedding_server import resolve_default_output_root, terminate_process, wait_for_server


class BackendManager:
    def __init__(
        self,
        server_cmd: list[str],
        backend_base_url: str,
        startup_timeout_s: float,
        log_dir: Path,
    ) -> None:
        self.server_cmd = server_cmd
        self.backend_base_url = backend_base_url.rstrip("/")
        self.startup_timeout_s = startup_timeout_s
        self.log_dir = log_dir
        self.lock = threading.Lock()
        self.process: subprocess.Popen[bytes] | None = None
        self.restart_count = 0

    def start(self) -> None:
        with self.lock:
            self._start_locked()

    def _start_locked(self) -> None:
        if self.process is not None and self.process.poll() is None:
            return
        self.restart_count += 1
        log_path = self.log_dir / f"llama-server-{self.restart_count:03d}.log"
        log_handle = log_path.open("wb")
        process = subprocess.Popen(
            self.server_cmd,
            stdin=subprocess.DEVNULL,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        log_handle.close()
        self.process = process
        wait_for_server(self.backend_base_url, process, self.startup_timeout_s)

    def restart(self) -> None:
        with self.lock:
            if self.process is not None:
                if self.process.poll() is None:
                    try:
                        os.killpg(self.process.pid, signal.SIGTERM)
                        self.process.wait(timeout=10)
                    except Exception:  # noqa: BLE001
                        terminate_process(self.process)
                self.process = None
            self._start_locked()

    def stop(self) -> None:
        with self.lock:
            if self.process is not None and self.process.poll() is None:
                try:
                    os.killpg(self.process.pid, signal.SIGTERM)
                    self.process.wait(timeout=10)
                except Exception:  # noqa: BLE001
                    terminate_process(self.process)
            self.process = None

    def request(self, method: str, path: str, body: bytes | None, headers: dict[str, str]) -> requests.Response:
        last_exc: Exception | None = None
        forward_path = path[3:] if path == "/v1" or path.startswith("/v1/") else path
        if not forward_path.startswith("/"):
            forward_path = "/" + forward_path
        for attempt in range(3):
            try:
                with self.lock:
                    self._start_locked()
                response = requests.request(
                    method,
                    self.backend_base_url + forward_path,
                    data=body,
                    headers=headers,
                    timeout=120,
                )
                return response
            except requests.RequestException as exc:
                last_exc = exc
                if attempt < 2:
                    self.restart()
                    continue
                raise
        raise RuntimeError(f"backend request failed: {last_exc}")


class ProxyHandler(BaseHTTPRequestHandler):
    manager: BackendManager

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        return

    def do_GET(self) -> None:  # noqa: N802
        self._proxy("GET")

    def do_POST(self) -> None:  # noqa: N802
        self._proxy("POST")

    def _proxy(self, method: str) -> None:
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length) if length else None
        headers = {"Content-Type": self.headers.get("Content-Type", "application/json")}
        try:
            response = self.manager.request(method, self.path, body, headers)
        except Exception as exc:  # noqa: BLE001
            payload = json.dumps({"error": f"embedding backend unavailable: {exc}"}).encode("utf-8")
            self.send_response(503)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        content = response.content
        self.send_response(response.status_code)
        self.send_header("Content-Type", response.headers.get("Content-Type", "application/json"))
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--llama-server-bin", type=Path, default=Path("/opt/homebrew/bin/llama-server"))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8099, help="Proxy port exposed to clients.")
    parser.add_argument("--backend-port", type=int, default=8199)
    parser.add_argument("--ctx-size", type=int, default=512)
    parser.add_argument("--pooling", default="mean")
    parser.add_argument("--embd-normalize", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=512)
    parser.add_argument("--ubatch-size", type=int, default=512)
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--startup-timeout-s", type=float, default=60.0)
    parser.add_argument("--run-id", default=f"llama-cpp-embedding-proxy-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--log-dir", type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER)
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

    proxy_base_url = f"http://{args.host}:{args.port}/v1"
    backend_base_url = f"http://{args.host}:{args.backend_port}/v1"
    log_dir = args.log_dir or (resolve_default_output_root() / "server-logs" / args.run_id)
    log_dir.mkdir(parents=True, exist_ok=True)
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
        str(args.backend_port),
        "--parallel",
        str(args.parallel),
        "--cont-batching",
    ]
    manifest = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "proxy_base_url": proxy_base_url,
        "backend_base_url": backend_base_url,
        "server_command": server_cmd,
        "command": command,
        "command_log": str(command_log_path),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    manager = BackendManager(server_cmd, backend_base_url, args.startup_timeout_s, log_dir)
    ProxyHandler.manager = manager
    httpd = ThreadingHTTPServer((args.host, args.port), ProxyHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    started = time.time()
    try:
        print(json.dumps({"status": "starting-proxy", "base_url": proxy_base_url, "log_dir": str(log_dir)}, indent=2))
        manager.start()
        thread.start()
        env = os.environ.copy()
        env["LLAMA_CPP_EMBEDDING_BASE_URL"] = proxy_base_url
        user_site = site.getusersitepackages()
        env["PYTHONPATH"] = user_site + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
        with command_log_path.open("wb") as command_log:
            child = subprocess.run(command, stdout=command_log, stderr=subprocess.STDOUT, env=env, check=False)
        result = {
            "status": "passed" if child.returncode == 0 else "failed",
            "command_returncode": child.returncode,
            "backend_restarts": manager.restart_count,
            "elapsed_s": round(time.time() - started, 3),
            "base_url": proxy_base_url,
            "log_dir": str(log_dir),
        }
        print(json.dumps(result, indent=2))
        return child.returncode
    finally:
        httpd.shutdown()
        httpd.server_close()
        manager.stop()


if __name__ == "__main__":
    sys.exit(main())
