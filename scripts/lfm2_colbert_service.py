#!/usr/bin/env python3
"""Serve LiquidAI/LFM2-ColBERT-350M as a local late-interaction retriever."""
from __future__ import annotations

import argparse
import json
import sys
import threading
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import numpy as np

try:
    import torch
except ModuleNotFoundError:  # pragma: no cover - torch is expected in the repo venv
    torch = None  # type: ignore[assignment]

from pylate import models


def require_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def require_int(payload: dict[str, Any], key: str, default: int) -> int:
    value = payload.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    if value < 1:
        raise ValueError(f"{key} must be >= 1")
    return value


def resolve_device(preferred: str) -> str:
    if preferred != "auto":
        return preferred
    if torch is not None and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


@dataclass
class ColbertStore:
    documents: list[dict[str, Any]] = field(default_factory=list)
    document_embeddings: dict[str, np.ndarray] = field(default_factory=dict)


class ColbertService:
    def __init__(self, model_id: str, device: str, local_files_only: bool) -> None:
        self.model_id = model_id
        self.device = resolve_device(device)
        self.local_files_only = local_files_only
        self.model = models.ColBERT(
            model_name_or_path=model_id,
            device=self.device,
            local_files_only=local_files_only,
        )
        self.default_index_id = "mem0_lfm2_colbert_350m"
        self._lock = threading.Lock()
        self._stores: dict[str, ColbertStore] = {self.default_index_id: ColbertStore()}

    def health(self) -> dict[str, Any]:
        return {
            "ok": True,
            "model_id": self.model_id,
            "index_id": self.default_index_id,
            "device": self.device,
            "local_files_only": self.local_files_only,
        }

    def index_documents(self, index_id: str, documents: list[dict[str, Any]]) -> dict[str, Any]:
        if not documents:
            raise ValueError("documents must not be empty")
        texts = [require_string(doc, "text") for doc in documents]
        doc_ids = [require_string(doc, "doc_id") for doc in documents]
        with self._lock:
            store = self._stores.setdefault(index_id, ColbertStore())
            encoded_docs = self._encode(texts, is_query=False)
            store.documents = [self._copy_document(doc, doc_id, text) for doc, doc_id, text in zip(documents, doc_ids, texts, strict=True)]
            store.document_embeddings = {doc_id: embedding for doc_id, embedding in zip(doc_ids, encoded_docs, strict=True)}
        return {"ok": True, "index_id": index_id, "document_count": len(documents)}

    def retrieve(self, query: str, documents: list[dict[str, Any]], top_k: int, index_id: str | None = None) -> dict[str, Any]:
        if not documents:
            raise ValueError("documents must not be empty")
        top_k = min(top_k, len(documents))
        query_embedding = self._encode([query], is_query=True)[0]
        texts = [require_string(doc, "text") for doc in documents]
        doc_ids = [require_string(doc, "doc_id") for doc in documents]
        embeddings = self._encode(texts, is_query=False)
        scored = []
        for doc, doc_id, text, embedding in zip(documents, doc_ids, texts, embeddings, strict=True):
            score = self._maxsim_score(query_embedding, embedding)
            scored.append(
                {
                    "doc_id": doc_id,
                    "score": float(score),
                    "text": text,
                    "metadata": {
                        **{key: value for key, value in doc.items() if key not in {"doc_id", "text"}},
                        "model_id": self.model_id,
                        "index_id": index_id or self.default_index_id,
                    },
                }
            )
        scored.sort(key=lambda item: item["score"], reverse=True)
        return {"results": scored[:top_k]}

    def _encode(self, texts: list[str], *, is_query: bool) -> list[np.ndarray]:
        outputs = self.model.encode(
            texts,
            is_query=is_query,
            convert_to_numpy=True,
            output_value="token_embeddings",
            normalize_embeddings=True,
        )
        embeddings: list[np.ndarray] = []
        for output in outputs:
            array = np.asarray(output, dtype=np.float32)
            if array.ndim != 2:
                raise ValueError(f"unexpected embedding rank: {array.shape}")
            embeddings.append(array)
        return embeddings

    @staticmethod
    def _maxsim_score(query_embedding: np.ndarray, document_embedding: np.ndarray) -> float:
        if query_embedding.size == 0 or document_embedding.size == 0:
            return 0.0
        similarities = query_embedding @ document_embedding.T
        return float(np.max(similarities, axis=1).sum())

    @staticmethod
    def _copy_document(document: dict[str, Any], doc_id: str, text: str) -> dict[str, Any]:
        return {
            "doc_id": doc_id,
            "text": text,
            "metadata": {key: value for key, value in document.items() if key not in {"doc_id", "text"}},
        }


class ColbertHandler(BaseHTTPRequestHandler):
    service: ColbertService

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        if getattr(self.server, "quiet", False):
            return
        super().log_message(format, *args)

    def do_GET(self) -> None:
        if self.path in {"/health", "/healthz"}:
            self.write_json(200, self.service.health())
            return
        self.write_json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path == "/index":
            self.handle_index()
            return
        if self.path == "/retrieve":
            self.handle_retrieve()
            return
        self.write_json(404, {"error": "not found"})

    def handle_index(self) -> None:
        try:
            payload = self.read_json()
            index_id = str(payload.get("index_id") or self.service.default_index_id)
            documents = payload.get("documents")
            if not isinstance(documents, list):
                raise ValueError("documents must be a list")
            result = self.service.index_documents(index_id, documents)
        except Exception as exc:  # noqa: BLE001
            self.write_json(400, {"error": str(exc)})
            return
        self.write_json(200, result)

    def handle_retrieve(self) -> None:
        try:
            payload = self.read_json()
            query = require_string(payload, "query")
            top_k = require_int(payload, "top_k", 3)
            documents = payload.get("documents")
            if not isinstance(documents, list):
                raise ValueError("documents must be a list")
            index_id = payload.get("index_id")
            if index_id is not None and not isinstance(index_id, str):
                raise ValueError("index_id must be a string when provided")
            result = self.service.retrieve(query, documents, top_k, index_id=index_id)
        except Exception as exc:  # noqa: BLE001
            self.write_json(400, {"error": str(exc)})
            return
        self.write_json(200, result)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or "0")
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--model", default="LiquidAI/LFM2-ColBERT-350M")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    service = ColbertService(args.model, args.device, args.local_files_only)
    ColbertHandler.service = service
    server = ThreadingHTTPServer((args.host, args.port), ColbertHandler)
    server.quiet = args.quiet  # type: ignore[attr-defined]
    try:
        print(
            f"lfm2 colbert service listening on http://{args.host}:{args.port} "
            f"(model={service.model_id}, device={service.device})",
            flush=True,
        )
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
