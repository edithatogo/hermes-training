#!/usr/bin/env python3
"""Guarded read-only mem0 search entrypoint for local agents."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from mem0_rerank_search import cli_safe_text, rerank_search_results, run_mem0_search
except ModuleNotFoundError:
    from scripts.mem0_rerank_search import cli_safe_text, rerank_search_results, run_mem0_search

DEFAULT_STRATEGY = "score_plus_created_at_rank_close_margin"
DEFAULT_RECENCY_WEIGHT = 0.20
DEFAULT_MLX_BGE_MODEL = "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit"
DEFAULT_RETRIEVER_SERVICE_URL = "http://127.0.0.1:8765"
MEM0_READ_CACHE_VERSION = 1


def select_strategy(mode: str) -> str:
    if mode == "vector":
        return "vector"
    if mode == "close-margin":
        return DEFAULT_STRATEGY
    if mode == "qwen3":
        return "qwen3_causal_lm"
    if mode == "mlx-bge":
        return "mlx_cross_encoder"
    if mode == "colbert":
        return "retriever_service"
    if mode == "colbert-qwen3":
        return "colbert_qwen3"
    raise ValueError(f"unsupported mode {mode!r}")


def build_output(
    query: str,
    tool: str,
    mode: str,
    strategy: str,
    results: list[dict[str, Any]],
    ranked: list[dict[str, Any]],
    search_latency_s: float,
    rerank_latency_s: float,
    total_latency_s: float,
    recency_weight: float,
    model: str,
    fallback_reason: str = "",
    raw: str = "",
    mem0_cache_hit: bool = False,
    mem0_cache_age_s: float = 0.0,
    source_mem0_search_latency_s: float = 0.0,
    document_fixture_path: str = "",
    retriever_service_url: str = "",
    retriever_index_id: str = "",
) -> dict[str, Any]:
    output = {
        "created_at": datetime.now(UTC).isoformat(),
        "tool": tool,
        "query": query,
        "mode": mode,
        "strategy": strategy,
        "model": model,
        "recency_weight": recency_weight,
        "read_only": True,
        "mutates_mem0_config": False,
        "input_count": len(results),
        "mem0_search_latency_s": round(search_latency_s, 3),
        "rerank_latency_s": round(rerank_latency_s, 3),
        "total_latency_s": round(total_latency_s, 3),
        "fallback_reason": fallback_reason,
        "mem0_cache_hit": mem0_cache_hit,
        "mem0_cache_age_s": round(mem0_cache_age_s, 3),
        "results": ranked,
    }
    if source_mem0_search_latency_s:
        output["source_mem0_search_latency_s"] = round(source_mem0_search_latency_s, 3)
    if document_fixture_path:
        output["document_fixture_path"] = document_fixture_path
    if retriever_service_url:
        output["retriever_service_url"] = retriever_service_url
    if retriever_index_id:
        output["retriever_index_id"] = retriever_index_id
    if raw:
        output["raw_mem0_output"] = raw
    return output


def resolve_default_cache_path() -> Path:
    env_cache_path = os.environ.get("HERMES_MEM0_READ_CACHE_PATH")
    if env_cache_path:
        return Path(env_cache_path)
    storage_root = os.environ.get("HERMES_STORAGE_ROOT")
    if storage_root:
        return Path(storage_root) / "hermes-cache" / "mem0-read-cache.json"
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD") / "hermes-cache" / "mem0-read-cache.json"
    return Path.cwd() / ".local-storage" / "hermes-cache" / "mem0-read-cache.json"


def config_fingerprint(path: Path | None = None) -> str:
    config_path = path or Path.home() / ".mem0" / "config.json"
    try:
        content = config_path.read_bytes()
    except FileNotFoundError:
        return "missing"
    return hashlib.sha256(content).hexdigest()


def cache_key(args: argparse.Namespace) -> str:
    payload = {
        "version": MEM0_READ_CACHE_VERSION,
        "tool": args.tool,
        "query": args.query,
        "cli_safe_query": cli_safe_text(args.query),
        "command": ["mem0", args.tool, "search", cli_safe_text(args.query)],
        "mem0_config_fingerprint": config_fingerprint(),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_cache(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"version": MEM0_READ_CACHE_VERSION, "entries": {}}
    if not isinstance(payload, dict) or payload.get("version") != MEM0_READ_CACHE_VERSION:
        return {"version": MEM0_READ_CACHE_VERSION, "entries": {}}
    entries = payload.get("entries")
    if not isinstance(entries, dict):
        payload["entries"] = {}
    return payload


def save_cache(path: Path, cache: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp_path.replace(path)


def cached_search(cache: dict[str, Any], key: str, ttl_s: float) -> tuple[list[dict[str, Any]], str, float, float] | None:
    if ttl_s <= 0:
        return None
    entry = cache.get("entries", {}).get(key)
    if not isinstance(entry, dict):
        return None
    cached_at = float(entry.get("cached_at", 0.0) or 0.0)
    age_s = time.time() - cached_at
    if age_s < 0 or age_s > ttl_s:
        return None
    results = entry.get("results")
    raw = entry.get("raw")
    source_latency_s = float(entry.get("source_mem0_search_latency_s", 0.0) or 0.0)
    if not isinstance(results, list) or not isinstance(raw, str):
        return None
    return results, raw, age_s, source_latency_s


def write_cache_entry(
    cache: dict[str, Any],
    key: str,
    results: list[dict[str, Any]],
    raw: str,
    source_mem0_search_latency_s: float,
) -> dict[str, Any]:
    cache.setdefault("version", MEM0_READ_CACHE_VERSION)
    entries = cache.setdefault("entries", {})
    if not isinstance(entries, dict):
        entries = {}
        cache["entries"] = entries
    entries[key] = {
        "cached_at": time.time(),
        "results": results,
        "raw": raw,
        "source_mem0_search_latency_s": source_mem0_search_latency_s,
    }
    return cache


def _document_id(document: dict[str, Any], index: int) -> str:
    value = document.get("id") or document.get("doc_id")
    if isinstance(value, str) and value:
        return value
    return f"fixture-doc-{index}"


def load_document_fixture(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        if isinstance(payload.get("documents"), list):
            raw_documents = payload["documents"]
        elif isinstance(payload.get("cases"), list):
            raw_documents = [
                doc
                for case in payload["cases"]
                if isinstance(case, dict) and isinstance(case.get("documents"), list)
                for doc in case["documents"]
            ]
        else:
            raise ValueError(f"{path}: expected documents or cases list")
    elif isinstance(payload, list):
        if all(isinstance(item, dict) and "documents" in item for item in payload):
            raw_documents = [
                doc
                for case in payload
                if isinstance(case.get("documents"), list)
                for doc in case["documents"]
            ]
        else:
            raw_documents = payload
    else:
        raise ValueError(f"{path}: expected JSON object or array")

    documents: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, raw in enumerate(raw_documents, 1):
        if not isinstance(raw, dict):
            continue
        text = raw.get("text") or raw.get("memory") or raw.get("content")
        if not isinstance(text, str) or not text.strip():
            continue
        doc_id = _document_id(raw, index)
        if doc_id in seen_ids:
            continue
        seen_ids.add(doc_id)
        documents.append(
            {
                "doc_id": doc_id,
                "text": text.strip(),
                "created_at": raw.get("created_at", ""),
                "metadata": {
                    key: value
                    for key, value in raw.items()
                    if key not in {"id", "doc_id", "text", "memory", "content"}
                },
            }
        )
    if not documents:
        raise ValueError(f"{path}: no usable documents")
    return documents


def run_retriever_service_search(
    query: str,
    documents: list[dict[str, Any]],
    service_url: str,
    top_k: int,
    timeout_s: float,
    index_id: str,
) -> tuple[list[dict[str, Any]], str, float]:
    payload: dict[str, Any] = {
        "query": query,
        "top_k": min(max(1, top_k), len(documents)),
        "documents": documents,
    }
    if index_id:
        payload["index_id"] = index_id
    started = time.time()
    request = Request(
        service_url.rstrip("/") + "/retrieve",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout_s) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as exc:
        raise RuntimeError(f"retriever service returned HTTP {exc.code}: {exc.read().decode('utf-8')}") from exc
    except URLError as exc:
        raise RuntimeError(f"retriever service unavailable: {exc.reason}") from exc
    latency_s = time.time() - started
    payload = json.loads(raw)
    raw_results = payload.get("results") if isinstance(payload, dict) else None
    if not isinstance(raw_results, list):
        raise RuntimeError("retriever service response missing results list")
    results: list[dict[str, Any]] = []
    for raw_result in raw_results:
        if not isinstance(raw_result, dict):
            continue
        metadata = raw_result.get("metadata") if isinstance(raw_result.get("metadata"), dict) else {}
        doc_id = str(raw_result.get("doc_id") or raw_result.get("id") or "")
        score = float(raw_result.get("score") or 0.0)
        results.append(
            {
                "id": doc_id,
                "memory": str(raw_result.get("text") or ""),
                "score": score,
                "created_at": metadata.get("created_at", ""),
                "metadata": metadata,
                "retriever_doc_id": doc_id,
                "retriever_score": score,
            }
        )
    return results, raw, latency_s


def run_guarded_read(args: argparse.Namespace) -> dict[str, Any]:
    total_started = time.time()
    strategy = select_strategy(args.mode)
    if strategy == "mlx_cross_encoder" and args.model == "Qwen/Qwen3-Reranker-0.6B":
        model = DEFAULT_MLX_BGE_MODEL
    elif strategy == "colbert_qwen3":
        model = args.model or "Qwen/Qwen3-Reranker-0.6B"
    else:
        model = args.model if strategy in {"qwen3_causal_lm", "mlx_cross_encoder"} else ""
    cache_ttl_s = float(getattr(args, "cache_ttl_s", 0.0) or 0.0)
    cache_arg = getattr(args, "cache_path", None)
    mlx_max_length = int(getattr(args, "mlx_max_length", 1024) or 1024)
    retriever_service_url = str(getattr(args, "retriever_service_url", DEFAULT_RETRIEVER_SERVICE_URL) or DEFAULT_RETRIEVER_SERVICE_URL)
    retriever_timeout_s = float(getattr(args, "retriever_timeout_s", args.timeout_s) or args.timeout_s)
    retriever_index_id = str(getattr(args, "retriever_index_id", "") or "")
    document_fixture = getattr(args, "document_fixture", None)
    cache_path = Path(cache_arg) if cache_arg else resolve_default_cache_path()
    key = cache_key(args) if cache_ttl_s > 0 else ""
    cache = load_cache(cache_path) if cache_ttl_s > 0 else {"version": MEM0_READ_CACHE_VERSION, "entries": {}}
    mem0_cache_hit = False
    mem0_cache_age_s = 0.0
    source_mem0_search_latency_s = 0.0
    refresh_cache = bool(getattr(args, "refresh_cache", False))
    hit = None if refresh_cache else cached_search(cache, key, cache_ttl_s)
    if strategy == "colbert_qwen3":
        if not document_fixture:
            raise ValueError("--document-fixture is required for colbert-qwen3 mode")
        documents = load_document_fixture(Path(document_fixture))
        retriever_top_k = int(getattr(args, "retriever_top_k", 8) or 8)
        results, raw, search_latency_s = run_retriever_service_search(
            args.query,
            documents,
            retriever_service_url,
            retriever_top_k,
            retriever_timeout_s,
            retriever_index_id,
        )
    elif hit is None:
        results, raw, search_latency_s = run_mem0_search(args.tool, args.query, args.timeout_s)
        if cache_ttl_s > 0:
            write_cache_entry(cache, key, results, raw, search_latency_s)
            save_cache(cache_path, cache)
    else:
        results, raw, mem0_cache_age_s, source_mem0_search_latency_s = hit
        search_latency_s = 0.0
        mem0_cache_hit = True
    fallback_reason = ""
    try:
        rerank_strategy = "qwen3_causal_lm" if strategy == "colbert_qwen3" else strategy
        ranked, rerank_latency_s = rerank_search_results(
            args.query,
            results,
            rerank_strategy,
            args.recency_weight,
            model,
            args.qwen3_device,
            args.qwen3_max_length,
            args.qwen3_instruction,
            args.qwen3_local_files_only,
            args.qwen3_server_url if rerank_strategy == "qwen3_causal_lm" else None,
            mlx_max_length,
            retriever_service_url if strategy == "retriever_service" else None,
            retriever_timeout_s,
        )
    except (RuntimeError, ValueError) as exc:
        if not args.fallback_to_vector:
            raise
        fallback_reason = str(exc)
        strategy = "vector"
        model = ""
        ranked, rerank_latency_s = rerank_search_results(
            args.query,
            results,
            strategy,
            args.recency_weight,
            None,
            args.qwen3_device,
            args.qwen3_max_length,
            args.qwen3_instruction,
            args.qwen3_local_files_only,
            None,
            mlx_max_length,
            None,
            retriever_timeout_s,
        )
    total_latency_s = time.time() - total_started
    output = build_output(
        args.query,
        args.tool,
        args.mode,
        strategy,
        results,
        ranked,
        search_latency_s,
        rerank_latency_s,
        total_latency_s,
        args.recency_weight,
        model,
        fallback_reason,
        raw if args.include_raw else "",
        mem0_cache_hit,
        mem0_cache_age_s,
        source_mem0_search_latency_s,
        str(document_fixture or ""),
        retriever_service_url if strategy in {"retriever_service", "colbert_qwen3"} else "",
        retriever_index_id if strategy in {"retriever_service", "colbert_qwen3"} else "",
    )
    if cache_ttl_s > 0:
        output["cache_path"] = str(cache_path)
    if strategy in {"retriever_service", "colbert_qwen3"}:
        output["retriever_service_url"] = retriever_service_url
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--tool", default="cmd")
    parser.add_argument(
        "--mode",
        choices=("close-margin", "vector", "qwen3", "mlx-bge", "colbert", "colbert-qwen3"),
        default="close-margin",
        help="Read mode. The default is the no-download close-margin reranker.",
    )
    parser.add_argument("--recency-weight", type=float, default=DEFAULT_RECENCY_WEIGHT)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--include-raw", action="store_true")
    parser.add_argument("--cache-path", type=Path, help="Optional JSON cache path for repeated read-only calls.")
    parser.add_argument("--cache-ttl-s", type=float, default=0.0, help="Enable cache hits for this many seconds. Default disables caching.")
    parser.add_argument("--refresh-cache", action="store_true", help="Bypass any existing cache entry and refresh it.")
    parser.add_argument(
        "--fallback-to-vector",
        action="store_true",
        help="Return vector ordering if the selected reranker fails.",
    )
    parser.add_argument("--model", default="Qwen/Qwen3-Reranker-0.6B")
    parser.add_argument("--mlx-max-length", type=int, default=1024)
    parser.add_argument("--retriever-service-url", default=DEFAULT_RETRIEVER_SERVICE_URL)
    parser.add_argument("--retriever-timeout-s", type=float, default=120.0)
    parser.add_argument("--retriever-index-id", default="")
    parser.add_argument("--retriever-top-k", type=int, default=8)
    parser.add_argument("--document-fixture", type=Path, help="JSON documents or retrieval suite for colbert-qwen3 mode.")
    parser.add_argument("--qwen3-device", default="auto")
    parser.add_argument("--qwen3-max-length", type=int, default=4096)
    parser.add_argument("--qwen3-local-files-only", action="store_true")
    parser.add_argument("--qwen3-server-url")
    parser.add_argument(
        "--qwen3-instruction",
        default="Retrieve memories that answer the query for a local Hermes agent.",
    )
    args = parser.parse_args()

    try:
        output = run_guarded_read(args)
    except (RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
