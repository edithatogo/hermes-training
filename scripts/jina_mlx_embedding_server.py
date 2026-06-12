#!/usr/bin/env python3
"""Serve a Jina MLX embedding model through a minimal OpenAI-compatible API."""
from __future__ import annotations

import argparse
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from run_jina_mlx_embedding_benchmark import ensure_repo, encode, load_model, repo_cache_name, resolve_default_repo_root


def json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def normalize_inputs(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError("input must be a string or list of strings")


def format_texts(task_type: str, texts: list[str]) -> list[str]:
    if task_type == "retrieval":
        return [f"Query: {text}" for text in texts]
    return texts


class EmbeddingHandler(BaseHTTPRequestHandler):
    server: "JinaEmbeddingServer"

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        if self.server.verbose:
            super().log_message(format, *args)

    def do_GET(self) -> None:  # noqa: N802
        if self.path.rstrip("/") == "/v1/models":
            json_response(
                self,
                200,
                {
                    "object": "list",
                    "data": [{"id": self.server.model_id, "object": "model", "owned_by": "local"}],
                },
            )
            return
        if self.path.rstrip("/") in {"", "/health", "/v1/health"}:
            json_response(self, 200, {"status": "ok", "model": self.server.model_id})
            return
        json_response(self, 404, {"error": {"message": f"unknown path: {self.path}"}})

    def do_POST(self) -> None:  # noqa: N802
        if self.path.rstrip("/") != "/v1/embeddings":
            json_response(self, 404, {"error": {"message": f"unknown path: {self.path}"}})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            inputs = normalize_inputs(payload.get("input"))
            requested_model = str(payload.get("model") or self.server.model_id)
            if requested_model != self.server.model_id:
                raise ValueError(f"unknown model {requested_model!r}; expected {self.server.model_id!r}")
            started = time.time()
            embeddings, _ = encode(self.server.model, format_texts(self.server.task_type, inputs), self.server.task_type)
            dimensions = payload.get("dimensions")
            if dimensions is not None:
                dimensions = int(dimensions)
                if dimensions != len(embeddings[0]):
                    raise ValueError(f"dimensions={dimensions} does not match model dimensions={len(embeddings[0])}")
            json_response(
                self,
                200,
                {
                    "object": "list",
                    "model": self.server.model_id,
                    "data": [
                        {"object": "embedding", "index": index, "embedding": embedding}
                        for index, embedding in enumerate(embeddings)
                    ],
                    "usage": {"prompt_tokens": 0, "total_tokens": 0},
                    "latency_s": round(time.time() - started, 6),
                },
            )
        except Exception as exc:  # noqa: BLE001
            json_response(self, 400, {"error": {"message": str(exc)}})


class JinaEmbeddingServer(ThreadingHTTPServer):
    model_id: str
    model: Any
    task_type: str
    verbose: bool


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="jinaai/jina-embeddings-v5-omni-small-text-matching-mlx")
    parser.add_argument("--task-type", default="text-matching", choices=["retrieval", "text-matching"])
    parser.add_argument("--revision", default="main")
    parser.add_argument("--repo-dir", type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8094)
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    repo_dir = args.repo_dir or (resolve_default_repo_root() / repo_cache_name(args.model))
    repo_dir = ensure_repo(args.model, repo_dir, args.revision, local_files_only=args.local_files_only)
    model = load_model(repo_dir)
    if hasattr(model, "switch_task"):
        model.switch_task(args.task_type)

    server = JinaEmbeddingServer((args.host, args.port), EmbeddingHandler)
    server.model_id = args.model
    server.model = model
    server.task_type = args.task_type
    server.verbose = args.verbose
    print(
        json.dumps(
            {
                "status": "ready",
                "model": args.model,
                "task_type": args.task_type,
                "repo_dir": str(repo_dir),
                "url": f"http://{args.host}:{args.port}/v1",
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
