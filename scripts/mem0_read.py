#!/usr/bin/env python3
"""Guarded read-only mem0 search entrypoint for local agents."""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import UTC, datetime
from typing import Any

try:
    from mem0_rerank_search import rerank_search_results, run_mem0_search
except ModuleNotFoundError:
    from scripts.mem0_rerank_search import rerank_search_results, run_mem0_search

DEFAULT_STRATEGY = "score_plus_created_at_rank_close_margin"
DEFAULT_RECENCY_WEIGHT = 0.20


def select_strategy(mode: str) -> str:
    if mode == "vector":
        return "vector"
    if mode == "close-margin":
        return DEFAULT_STRATEGY
    if mode == "qwen3":
        return "qwen3_causal_lm"
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
        "results": ranked,
    }
    if raw:
        output["raw_mem0_output"] = raw
    return output


def run_guarded_read(args: argparse.Namespace) -> dict[str, Any]:
    total_started = time.time()
    strategy = select_strategy(args.mode)
    results, raw, search_latency_s = run_mem0_search(args.tool, args.query, args.timeout_s)
    model = args.model if strategy == "qwen3_causal_lm" else ""
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
        )
    total_latency_s = time.time() - total_started
    return build_output(
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
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--tool", default="cmd")
    parser.add_argument(
        "--mode",
        choices=("close-margin", "vector", "qwen3"),
        default="close-margin",
        help="Read mode. The default is the no-download close-margin reranker.",
    )
    parser.add_argument("--recency-weight", type=float, default=DEFAULT_RECENCY_WEIGHT)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--include-raw", action="store_true")
    parser.add_argument(
        "--fallback-to-vector",
        action="store_true",
        help="Return vector ordering if the selected reranker fails.",
    )
    parser.add_argument("--model", default="Qwen/Qwen3-Reranker-0.6B")
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
