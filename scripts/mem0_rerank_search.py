#!/usr/bin/env python3
"""Run mem0 search and apply a local reranking strategy without changing mem0 config."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from typing import Any

try:
    from mem0_rerank_lib import parse_mem0_search_output, rerank_results
    from run_fixed_reranking_benchmark import qwen3_causal_lm_rerank
except ModuleNotFoundError:
    from scripts.mem0_rerank_lib import parse_mem0_search_output, rerank_results
    from scripts.run_fixed_reranking_benchmark import qwen3_causal_lm_rerank


def cli_safe_text(text: str) -> str:
    """Avoid a mem0 CLI search quoting bug around ASCII apostrophes."""
    return text.replace("'", " ")


def run_mem0_search(tool: str, query: str, timeout_s: float) -> tuple[list[dict[str, Any]], str, float]:
    started = time.time()
    completed = subprocess.run(
        ["mem0", tool, "search", cli_safe_text(query)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
        check=False,
    )
    latency_s = time.time() - started
    if completed.returncode != 0:
        raise RuntimeError(f"mem0 {tool} search failed with {completed.returncode}:\n{completed.stdout}")
    return parse_mem0_search_output(completed.stdout), completed.stdout, latency_s


def rerank_search_results(
    query: str,
    results: list[dict[str, Any]],
    strategy: str,
    recency_weight: float,
    model: str | None,
    qwen3_device: str,
    qwen3_max_length: int,
    qwen3_instruction: str,
) -> tuple[list[dict[str, Any]], float]:
    if not results:
        return [], 0.0
    if strategy == "qwen3_causal_lm":
        if not model:
            raise ValueError("--model is required for qwen3_causal_lm")
        return qwen3_causal_lm_rerank(
            model,
            query,
            results,
            qwen3_device,
            qwen3_max_length,
            qwen3_instruction,
        )
    rerank_started = time.time()
    ranked = rerank_results(results, strategy, recency_weight)
    return ranked, time.time() - rerank_started


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--tool", default="cmd")
    parser.add_argument(
        "--strategy",
        choices=(
            "vector",
            "score_plus_recency",
            "score_plus_created_at_rank",
            "score_plus_created_at_rank_close_margin",
            "benchmark_order",
            "qwen3_causal_lm",
        ),
        default="score_plus_created_at_rank",
    )
    parser.add_argument("--model", help="Reranker model id for learned strategies.")
    parser.add_argument("--qwen3-device", default="auto", help="Device for qwen3_causal_lm: auto, mps, or cpu.")
    parser.add_argument("--qwen3-max-length", type=int, default=8192)
    parser.add_argument(
        "--qwen3-instruction",
        default="Retrieve memories that answer the query for a local Hermes agent.",
    )
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--include-raw", action="store_true")
    args = parser.parse_args()

    total_started = time.time()
    results, raw, search_latency_s = run_mem0_search(args.tool, args.query, args.timeout_s)
    try:
        ranked, rerank_latency_s = rerank_search_results(
            args.query,
            results,
            args.strategy,
            args.recency_weight,
            args.model,
            args.qwen3_device,
            args.qwen3_max_length,
            args.qwen3_instruction,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    total_latency_s = time.time() - total_started
    output = {
        "created_at": datetime.now(UTC).isoformat(),
        "tool": args.tool,
        "query": args.query,
        "strategy": args.strategy,
        "model": args.model or "",
        "recency_weight": args.recency_weight,
        "latency_s": round(search_latency_s, 3),
        "mem0_search_latency_s": round(search_latency_s, 3),
        "rerank_latency_s": round(rerank_latency_s, 3),
        "total_latency_s": round(total_latency_s, 3),
        "input_count": len(results),
        "results": ranked,
    }
    if args.strategy == "qwen3_causal_lm":
        output["qwen3_device"] = args.qwen3_device
        output["qwen3_max_length"] = args.qwen3_max_length
        output["qwen3_instruction"] = args.qwen3_instruction
    if args.include_raw:
        output["raw_mem0_output"] = raw
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
