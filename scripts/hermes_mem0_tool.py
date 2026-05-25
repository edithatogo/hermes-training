#!/usr/bin/env python3
"""Stable command wrapper for Hermes-agent explicit mem0 reads."""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

try:
    from mem0_read import run_guarded_read
except ModuleNotFoundError:
    from scripts.mem0_read import run_guarded_read

VALID_MODES = {"close-margin", "vector", "qwen3"}
DEFAULT_CACHE_TTL_S = 300.0


def load_payload(stdin_text: str, query: str | None) -> dict[str, Any]:
    if query:
        return {"query": query}
    text = stdin_text.strip()
    if not text:
        raise ValueError("query is required via --query or stdin JSON")
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("stdin JSON must be an object")
    return payload


def bool_value(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def float_value(value: Any, default: float) -> float:
    if value is None or value == "":
        return default
    return float(value)


def int_value(value: Any, default: int) -> int:
    if value is None or value == "":
        return default
    return int(value)


def build_read_args(args: argparse.Namespace, payload: dict[str, Any]) -> argparse.Namespace:
    query = payload.get("query")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("payload.query must be a non-empty string")
    mode = str(payload.get("mode") or args.mode).strip()
    if mode not in VALID_MODES:
        raise ValueError(f"mode must be one of {sorted(VALID_MODES)}")
    cache_ttl_s = float_value(payload.get("cache_ttl_s"), args.cache_ttl_s)
    if cache_ttl_s < 0:
        raise ValueError("cache_ttl_s must be >= 0")
    timeout_s = float_value(payload.get("timeout_s"), args.timeout_s)
    if timeout_s <= 0:
        raise ValueError("timeout_s must be > 0")
    qwen3_max_length = int_value(payload.get("qwen3_max_length"), args.qwen3_max_length)
    if qwen3_max_length <= 0:
        raise ValueError("qwen3_max_length must be > 0")
    return argparse.Namespace(
        query=query.strip(),
        tool=str(payload.get("tool") or args.tool),
        mode=mode,
        timeout_s=timeout_s,
        recency_weight=float_value(payload.get("recency_weight"), args.recency_weight),
        model=str(payload.get("model") or args.model),
        qwen3_device=str(payload.get("qwen3_device") or args.qwen3_device),
        qwen3_max_length=qwen3_max_length,
        qwen3_instruction=str(payload.get("qwen3_instruction") or args.qwen3_instruction),
        qwen3_local_files_only=bool_value(payload.get("qwen3_local_files_only"), args.qwen3_local_files_only),
        qwen3_server_url=payload.get("qwen3_server_url") or args.qwen3_server_url,
        fallback_to_vector=bool_value(payload.get("fallback_to_vector"), args.fallback_to_vector),
        include_raw=bool_value(payload.get("include_raw"), args.include_raw),
        cache_path=payload.get("cache_path") or args.cache_path,
        cache_ttl_s=cache_ttl_s,
        refresh_cache=bool_value(payload.get("refresh_cache"), args.refresh_cache),
    )


def render_tool_result(read_output: dict[str, Any]) -> dict[str, Any]:
    results = read_output.get("results") if isinstance(read_output.get("results"), list) else []
    memories = []
    for item in results:
        if not isinstance(item, dict):
            continue
        memories.append(
            {
                "id": item.get("id", ""),
                "memory": item.get("memory", ""),
                "score": item.get("score"),
                "rerank_score": item.get("rerank_score"),
                "created_at": item.get("created_at", ""),
                "metadata": item.get("metadata", {}),
            }
        )
    return {
        "ok": True,
        "tool": "hermes_mem0_read",
        "read_only": True,
        "mutates_mem0_config": False,
        "query": read_output.get("query", ""),
        "mode": read_output.get("mode", ""),
        "strategy": read_output.get("strategy", ""),
        "mem0_cache_hit": read_output.get("mem0_cache_hit", False),
        "input_count": read_output.get("input_count", 0),
        "latency": {
            "total_s": read_output.get("total_latency_s", 0.0),
            "mem0_search_s": read_output.get("mem0_search_latency_s", 0.0),
            "rerank_s": read_output.get("rerank_latency_s", 0.0),
        },
        "memories": memories,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Memory lookup query. Overrides stdin JSON when provided.")
    parser.add_argument("--tool", default="cmd")
    parser.add_argument("--mode", choices=sorted(VALID_MODES), default="close-margin")
    parser.add_argument("--cache-path")
    parser.add_argument("--cache-ttl-s", type=float, default=DEFAULT_CACHE_TTL_S)
    parser.add_argument("--refresh-cache", action="store_true")
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument("--include-raw", action="store_true")
    parser.add_argument("--fallback-to-vector", action="store_true")
    parser.add_argument("--model", default="Qwen/Qwen3-Reranker-0.6B")
    parser.add_argument("--qwen3-device", default="auto")
    parser.add_argument("--qwen3-max-length", type=int, default=4096)
    parser.add_argument("--qwen3-local-files-only", action="store_true")
    parser.add_argument("--qwen3-server-url")
    parser.add_argument("--qwen3-instruction", default="Retrieve memories that answer the query for a local Hermes agent.")
    args = parser.parse_args()

    try:
        payload = load_payload(sys.stdin.read() if not sys.stdin.isatty() else "", args.query)
        read_args = build_read_args(args, payload)
        result = render_tool_result(run_guarded_read(read_args))
    except (json.JSONDecodeError, RuntimeError, ValueError) as exc:
        result = {
            "ok": False,
            "tool": "hermes_mem0_read",
            "read_only": True,
            "mutates_mem0_config": False,
            "error": str(exc),
        }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
