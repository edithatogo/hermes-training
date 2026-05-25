#!/usr/bin/env python3
"""Run repeated guarded mem0 reads and summarize agent-facing latency."""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from mem0_read import run_guarded_read
    from run_fixed_reranking_benchmark import percentile
except ModuleNotFoundError:
    from scripts.mem0_read import run_guarded_read
    from scripts.run_fixed_reranking_benchmark import percentile

DEFAULT_QUERIES = [
    "What is the active mem0 Qdrant collection?",
    "Which embedding model is configured for local mem0?",
    "Which extraction model is currently configured for local mem0?",
    "What should be used as the rollback path for mem0 reads?",
    "Which reranker is safest for live recency-sensitive mem0 reads?",
]


def resolve_default_output_root() -> Path:
    env_eval_root = os.environ.get("HERMES_EVAL_ROOT")
    if env_eval_root:
        return Path(env_eval_root)
    storage_root = os.environ.get("HERMES_STORAGE_ROOT")
    if storage_root:
        return Path(storage_root) / "hermes-evals"
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD") / "hermes-evals"
    return Path.cwd() / ".local-storage" / "hermes-evals"


def load_queries(path: Path | None, inline_queries: list[str]) -> list[str]:
    if inline_queries:
        return inline_queries
    if not path:
        return DEFAULT_QUERIES
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"{path}: expected a JSON array")
    queries: list[str] = []
    for index, item in enumerate(payload, 1):
        if isinstance(item, str):
            queries.append(item)
        elif isinstance(item, dict) and isinstance(item.get("query"), str):
            queries.append(item["query"])
        else:
            raise ValueError(f"{path}: query {index} must be a string or object with a string query field")
    return queries


def save_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def summarize_latency_group(rows: list[dict[str, Any]]) -> dict[str, Any]:
    totals = [float(row["total_latency_s"]) for row in rows]
    searches = [float(row["mem0_search_latency_s"]) for row in rows]
    reranks = [float(row["rerank_latency_s"]) for row in rows]
    return {
        "count": len(rows),
        "total_latency_p50_s": percentile(totals, 0.50),
        "total_latency_p95_s": percentile(totals, 0.95),
        "total_latency_mean_s": statistics.fmean(totals) if totals else 0.0,
        "mem0_search_latency_p50_s": percentile(searches, 0.50),
        "mem0_search_latency_p95_s": percentile(searches, 0.95),
        "rerank_latency_p50_s": percentile(reranks, 0.50),
        "rerank_latency_p95_s": percentile(reranks, 0.95),
    }


def summarize(rows: list[dict[str, Any]], run_id: str, output_dir: Path, queries: list[str], args: argparse.Namespace) -> dict[str, Any]:
    totals = [float(row["total_latency_s"]) for row in rows]
    searches = [float(row["mem0_search_latency_s"]) for row in rows]
    reranks = [float(row["rerank_latency_s"]) for row in rows]
    input_counts = [int(row["input_count"]) for row in rows]
    fallbacks = [row for row in rows if row.get("fallback_reason")]
    cache_hits = [row for row in rows if row.get("mem0_cache_hit")]
    cold_rows = [row for row in rows if not row.get("mem0_cache_hit")]
    cold_summary = summarize_latency_group(cold_rows)
    cache_summary = summarize_latency_group(cache_hits)
    cache_p50 = float(cache_summary["total_latency_p50_s"])
    return {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "output_dir": str(output_dir),
        "tool": args.tool,
        "mode": args.mode,
        "strategy": rows[0].get("strategy", "") if rows else "",
        "model": args.model if args.mode == "qwen3" else "",
        "read_only": True,
        "mutates_mem0_config": False,
        "query_count": len(queries),
        "iterations": args.iterations,
        "case_count": len(rows),
        "success_count": len(rows),
        "fallback_count": len(fallbacks),
        "mem0_cache_hit_count": len(cache_hits),
        "input_count_min": min(input_counts, default=0),
        "input_count_max": max(input_counts, default=0),
        "multi_result_count": sum(1 for count in input_counts if count > 1),
        "singleton_count": sum(1 for count in input_counts if count == 1),
        "empty_count": sum(1 for count in input_counts if count == 0),
        "total_latency_p50_s": percentile(totals, 0.50),
        "total_latency_p95_s": percentile(totals, 0.95),
        "total_latency_mean_s": statistics.fmean(totals) if totals else 0.0,
        "mem0_search_latency_p50_s": percentile(searches, 0.50),
        "mem0_search_latency_p95_s": percentile(searches, 0.95),
        "rerank_latency_p50_s": percentile(reranks, 0.50),
        "rerank_latency_p95_s": percentile(reranks, 0.95),
        "scenario_summaries": {
            "cold": cold_summary,
            "cache_hit": cache_summary,
        },
        "cache_speedup_p50_ratio": (float(cold_summary["total_latency_p50_s"]) / cache_p50) if cache_p50 > 0 else None,
        "queries": queries,
    }


def render_markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# mem0 Read Latency Probe: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        f"Mode: `{summary['mode']}`",
        f"Strategy: `{summary['strategy']}`",
        f"Output: `{summary['output_dir']}`",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Cases | {summary['case_count']} |",
        f"| Success count | {summary['success_count']} |",
        f"| Fallback count | {summary['fallback_count']} |",
        f"| mem0 cache hit count | {summary['mem0_cache_hit_count']} |",
        f"| Input count min / max | {summary['input_count_min']} / {summary['input_count_max']} |",
        f"| Multi-result count | {summary['multi_result_count']} |",
        f"| Singleton count | {summary['singleton_count']} |",
        f"| Empty count | {summary['empty_count']} |",
        f"| Total latency p50 | {summary['total_latency_p50_s']:.3f}s |",
        f"| Total latency p95 | {summary['total_latency_p95_s']:.3f}s |",
        f"| mem0 search latency p50 | {summary['mem0_search_latency_p50_s']:.3f}s |",
        f"| mem0 search latency p95 | {summary['mem0_search_latency_p95_s']:.3f}s |",
        f"| Rerank latency p50 | {summary['rerank_latency_p50_s']:.3f}s |",
        "",
        "## Cold vs Cache",
        "",
        "| Scenario | Count | Total p50 | Total p95 | mem0 search p50 | Rerank p50 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for scenario, metrics in summary["scenario_summaries"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    scenario,
                    str(metrics["count"]),
                    f"{metrics['total_latency_p50_s']:.3f}s",
                    f"{metrics['total_latency_p95_s']:.3f}s",
                    f"{metrics['mem0_search_latency_p50_s']:.3f}s",
                    f"{metrics['rerank_latency_p50_s']:.3f}s",
                ]
            )
            + " |"
        )
    speedup = summary.get("cache_speedup_p50_ratio")
    lines.extend(
        [
            "",
            f"Cache p50 speedup ratio: `{speedup:.1f}x`" if isinstance(speedup, (float, int)) else "Cache p50 speedup ratio: sub-millisecond cache hits rounded to `0.000s`.",
            "",
            "## Cases",
            "",
            "| Query | Input count | Cache hit | Total latency | Fallback |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['query']} | {row['input_count']} | {row.get('mem0_cache_hit', False)} | {float(row['total_latency_s']):.3f}s | {row.get('fallback_reason', '')} |"
        )
    lines.extend(
        [
            "",
            "## Decision Use",
            "",
            "Use this probe for agent UX checks before wiring the guarded read wrapper into Hermes runtime. It is read-only and does not change mem0 defaults.",
            "",
        ]
    )
    return "\n".join(lines)


def build_read_args(args: argparse.Namespace, query: str) -> argparse.Namespace:
    return argparse.Namespace(
        query=query,
        tool=args.tool,
        mode=args.mode,
        timeout_s=args.timeout_s,
        recency_weight=args.recency_weight,
        model=args.model,
        qwen3_device=args.qwen3_device,
        qwen3_max_length=args.qwen3_max_length,
        qwen3_instruction=args.qwen3_instruction,
        qwen3_local_files_only=args.qwen3_local_files_only,
        qwen3_server_url=args.qwen3_server_url,
        fallback_to_vector=args.fallback_to_vector,
        include_raw=args.include_raw,
        cache_path=args.cache_path,
        cache_ttl_s=args.cache_ttl_s,
        refresh_cache=args.refresh_cache,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queries", type=Path, help="JSON array of query strings or objects with a query field.")
    parser.add_argument("--query", action="append", default=[], help="Inline query. Can be repeated.")
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--run-id", default=f"mem0-read-latency-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--tool", default="cmd")
    parser.add_argument("--mode", choices=("close-margin", "vector", "qwen3"), default="close-margin")
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--include-raw", action="store_true")
    parser.add_argument("--cache-path", type=Path, help="Optional JSON cache path passed through to mem0_read.py.")
    parser.add_argument("--cache-ttl-s", type=float, default=0.0, help="Enable mem0 search cache hits for this many seconds.")
    parser.add_argument("--refresh-cache", action="store_true", help="Refresh cache entries during the probe.")
    parser.add_argument("--fallback-to-vector", action="store_true")
    parser.add_argument("--model", default="Qwen/Qwen3-Reranker-0.6B")
    parser.add_argument("--qwen3-device", default="auto")
    parser.add_argument("--qwen3-max-length", type=int, default=4096)
    parser.add_argument("--qwen3-local-files-only", action="store_true")
    parser.add_argument("--qwen3-server-url")
    parser.add_argument("--qwen3-instruction", default="Retrieve memories that answer the query for a local Hermes agent.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.iterations < 1:
        raise SystemExit("--iterations must be >= 1")
    queries = load_queries(args.queries, args.query)
    if not queries:
        raise SystemExit("at least one query is required")

    output_dir = args.output_dir or (resolve_default_output_root() / "mem0-read-latency" / args.run_id)
    if args.dry_run:
        print(json.dumps({"run_id": args.run_id, "output_dir": str(output_dir), "queries": queries}, indent=2))
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for iteration in range(1, args.iterations + 1):
        for query_index, query in enumerate(queries, 1):
            print(f"  [{iteration}/{args.iterations} {query_index}/{len(queries)}] {query}")
            output = run_guarded_read(build_read_args(args, query))
            output["iteration"] = iteration
            output["query_index"] = query_index
            rows.append(output)

    summary = summarize(rows, args.run_id, output_dir, queries, args)
    save_jsonl(output_dir / "results.jsonl", rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_markdown(summary, rows), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"results: {output_dir / 'results.jsonl'}")
    print(f"summary: {output_dir / 'summary.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
