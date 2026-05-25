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

from mem0_rerank_lib import parse_mem0_search_output, rerank_results


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
        ),
        default="score_plus_created_at_rank",
    )
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--include-raw", action="store_true")
    args = parser.parse_args()

    results, raw, latency_s = run_mem0_search(args.tool, args.query, args.timeout_s)
    ranked = rerank_results(results, args.strategy, args.recency_weight)
    output = {
        "created_at": datetime.now(UTC).isoformat(),
        "tool": args.tool,
        "query": args.query,
        "strategy": args.strategy,
        "recency_weight": args.recency_weight,
        "latency_s": round(latency_s, 3),
        "input_count": len(results),
        "results": ranked,
    }
    if args.include_raw:
        output["raw_mem0_output"] = raw
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
