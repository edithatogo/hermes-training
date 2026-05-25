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

try:
    from mem0_rerank_search import cli_safe_text, rerank_search_results, run_mem0_search
except ModuleNotFoundError:
    from scripts.mem0_rerank_search import cli_safe_text, rerank_search_results, run_mem0_search

DEFAULT_STRATEGY = "score_plus_created_at_rank_close_margin"
DEFAULT_RECENCY_WEIGHT = 0.20
DEFAULT_MLX_BGE_MODEL = "flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit"
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


def run_guarded_read(args: argparse.Namespace) -> dict[str, Any]:
    total_started = time.time()
    strategy = select_strategy(args.mode)
    if strategy == "mlx_cross_encoder" and args.model == "Qwen/Qwen3-Reranker-0.6B":
        model = DEFAULT_MLX_BGE_MODEL
    else:
        model = args.model if strategy in {"qwen3_causal_lm", "mlx_cross_encoder"} else ""
    cache_ttl_s = float(getattr(args, "cache_ttl_s", 0.0) or 0.0)
    cache_arg = getattr(args, "cache_path", None)
    mlx_max_length = int(getattr(args, "mlx_max_length", 1024) or 1024)
    cache_path = Path(cache_arg) if cache_arg else resolve_default_cache_path()
    key = cache_key(args) if cache_ttl_s > 0 else ""
    cache = load_cache(cache_path) if cache_ttl_s > 0 else {"version": MEM0_READ_CACHE_VERSION, "entries": {}}
    mem0_cache_hit = False
    mem0_cache_age_s = 0.0
    source_mem0_search_latency_s = 0.0
    refresh_cache = bool(getattr(args, "refresh_cache", False))
    hit = None if refresh_cache else cached_search(cache, key, cache_ttl_s)
    if hit is None:
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
        ranked, rerank_latency_s = rerank_search_results(
            args.query,
            results,
            strategy,
            args.recency_weight,
            model,
            args.qwen3_device,
            args.qwen3_max_length,
            args.qwen3_instruction,
            args.qwen3_local_files_only,
            args.qwen3_server_url if strategy == "qwen3_causal_lm" else None,
            mlx_max_length,
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
    )
    if cache_ttl_s > 0:
        output["cache_path"] = str(cache_path)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--tool", default="cmd")
    parser.add_argument(
        "--mode",
        choices=("close-margin", "vector", "qwen3", "mlx-bge"),
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
