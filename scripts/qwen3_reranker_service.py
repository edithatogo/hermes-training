#!/usr/bin/env python3
"""Serve the Qwen3 causal-LM reranker as a warm local HTTP helper."""
from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

try:
    from run_fixed_reranking_benchmark import qwen3_causal_lm_rerank
except ModuleNotFoundError:
    from scripts.run_fixed_reranking_benchmark import qwen3_causal_lm_rerank


class RerankerHandler(BaseHTTPRequestHandler):
    default_model = "Qwen/Qwen3-Reranker-0.6B"
    default_device = "auto"
    default_max_length = 8192
    default_instruction = "Retrieve memories that answer the query for a local Hermes agent."
    default_local_files_only = False

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        if getattr(self.server, "quiet", False):
            return
        super().log_message(format, *args)

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self.write_json(200, {"status": "ok", "model": self.default_model})
            return
        self.write_json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/rerank":
            self.write_json(404, {"error": "not found"})
            return
        try:
            payload = self.read_json()
            query = require_string(payload, "query")
            results = payload.get("results")
            if not isinstance(results, list):
                raise ValueError("results must be a list")
            model = str(payload.get("model") or self.default_model)
            device = str(payload.get("device") or self.default_device)
            max_length = int(payload.get("max_length") or self.default_max_length)
            instruction = str(payload.get("instruction") or self.default_instruction)
            local_files_only = bool(payload.get("local_files_only", self.default_local_files_only))
            ranked, latency_s = qwen3_causal_lm_rerank(
                model,
                query,
                results,
                device,
                max_length,
                instruction,
                local_files_only=local_files_only,
            )
        except Exception as exc:  # noqa: BLE001
            self.write_json(400, {"error": str(exc)})
            return
        self.write_json(
            200,
            {
                "model": model,
                "device": device,
                "max_length": max_length,
                "local_files_only": local_files_only,
                "rerank_latency_s": round(latency_s, 3),
                "input_count": len(results),
                "results": ranked,
            },
        )

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or "0")
        data = self.rfile.read(length)
        payload = json.loads(data.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("request body must be a JSON object")
        return payload

    def write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def require_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--model", default=RerankerHandler.default_model)
    parser.add_argument("--device", default=RerankerHandler.default_device)
    parser.add_argument("--max-length", type=int, default=RerankerHandler.default_max_length)
    parser.add_argument("--instruction", default=RerankerHandler.default_instruction)
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    RerankerHandler.default_model = args.model
    RerankerHandler.default_device = args.device
    RerankerHandler.default_max_length = args.max_length
    RerankerHandler.default_instruction = args.instruction
    RerankerHandler.default_local_files_only = args.local_files_only
    server = ThreadingHTTPServer((args.host, args.port), RerankerHandler)
    server.quiet = args.quiet  # type: ignore[attr-defined]
    try:
        print(f"qwen3 reranker service listening on http://{args.host}:{args.port}", flush=True)
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
