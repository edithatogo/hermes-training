#!/usr/bin/env python3
"""Run a local mem0 add/search benchmark through the mem0 CLI."""
from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mem0_rerank_lib import rerank_results


VALID_CATEGORIES = {"direct_recall", "recency_conflict", "distractor_resistance", "tool_state_recall"}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def extract_first_json_object(text: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise ValueError(f"mem0 output did not contain a JSON object: {text[:500]}")


def run_mem0(args: list[str], timeout_s: float) -> tuple[dict[str, Any], float, str]:
    started = time.time()
    completed = subprocess.run(
        ["mem0", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
        check=False,
    )
    latency_s = time.time() - started
    if completed.returncode != 0:
        raise RuntimeError(f"mem0 {' '.join(args)} failed with {completed.returncode}:\n{completed.stdout}")
    return extract_first_json_object(completed.stdout), latency_s, completed.stdout


def cli_safe_text(text: str) -> str:
    """Avoid a mem0 CLI search quoting bug around ASCII apostrophes."""
    return text.replace("'", " ")


def validate_suite(suite: list[Any], suite_path: Path) -> None:
    if not suite:
        raise ValueError(f"{suite_path}: empty mem0 benchmark suite")
    seen_ids: set[str] = set()
    for index, case in enumerate(suite, 1):
        if not isinstance(case, dict):
            raise ValueError(f"{suite_path}:{index}: each case must be an object")
        missing = {"id", "category", "setup_memories", "query", "expected"} - set(case)
        if missing:
            raise ValueError(f"{suite_path}:{index}: missing keys {sorted(missing)}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{suite_path}:{index}: id must be a non-empty string")
        if case_id in seen_ids:
            raise ValueError(f"{suite_path}: duplicate case id {case_id}")
        seen_ids.add(case_id)
        if case["category"] not in VALID_CATEGORIES:
            raise ValueError(f"{case_id}: unsupported category {case['category']!r}")
        memories = case["setup_memories"]
        if not isinstance(memories, list) or not memories or not all(isinstance(item, str) and item for item in memories):
            raise ValueError(f"{case_id}: setup_memories must be a non-empty list of strings")
        if not isinstance(case["query"], str) or not case["query"]:
            raise ValueError(f"{case_id}: query must be a non-empty string")
        expected = case["expected"]
        if not isinstance(expected, dict):
            raise ValueError(f"{case_id}: expected must be an object")
        must_any = expected.get("must_retrieve_any")
        if not isinstance(must_any, list) or not must_any or not all(isinstance(item, str) and item for item in must_any):
            raise ValueError(f"{case_id}: expected.must_retrieve_any must be a non-empty list of strings")
        must_not = expected.get("must_not_retrieve_any", [])
        if not isinstance(must_not, list) or not all(isinstance(item, str) and item for item in must_not):
            raise ValueError(f"{case_id}: expected.must_not_retrieve_any must be a list of strings")
        top_contains = expected.get("top_result_should_contain")
        if top_contains is not None and not isinstance(top_contains, str):
            raise ValueError(f"{case_id}: top_result_should_contain must be a string")


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    sorted_values = sorted(values)
    index = (len(sorted_values) - 1) * pct
    lower = int(index)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = index - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def result_memories(search_response: dict[str, Any]) -> list[str]:
    rows = search_response.get("results", [])
    if not isinstance(rows, list):
        return []
    memories: list[str] = []
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("memory"), str):
            memories.append(row["memory"])
    return memories


def result_objects(search_response: dict[str, Any]) -> list[dict[str, Any]]:
    rows = search_response.get("results", [])
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def score_case(case: dict[str, Any], memories: list[str]) -> dict[str, Any]:
    joined = "\n".join(memories).lower()
    top = memories[0].lower() if memories else ""
    expected = case["expected"]
    must_any = [item.lower() for item in expected["must_retrieve_any"]]
    must_not = [item.lower() for item in expected.get("must_not_retrieve_any", [])]
    top_contains = expected.get("top_result_should_contain")

    retrieved = any(item in joined for item in must_any)
    forbidden_hit = any(item in joined for item in must_not)
    top_ok = True
    if top_contains:
        top_ok = top_contains.lower() in top

    passed = retrieved and not forbidden_hit and top_ok
    return {
        "pass": passed,
        "retrieved_expected": retrieved,
        "forbidden_hit": forbidden_hit,
        "top_result_ok": top_ok,
        "top_result": memories[0] if memories else "",
        "result_count": len(memories),
    }


def render_summary_markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# mem0 Memory Benchmark: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Cases | {summary['cases']} |",
        f"| Pass rate | {summary['pass_rate']:.3f} |",
        f"| Recall@k | {summary['recall_at_k']:.3f} |",
        f"| Top-1 expected rate | {summary['top1_expected_rate']:.3f} |",
        f"| Recency conflict pass rate | {summary['recency_conflict_pass_rate']:.3f} |",
        f"| Distractor resistance pass rate | {summary['distractor_resistance_pass_rate']:.3f} |",
        f"| Add latency p50 | {summary['add_latency_p50_s']:.3f}s |",
        f"| Search latency p50 | {summary['search_latency_p50_s']:.3f}s |",
        f"| Search latency p95 | {summary['search_latency_p95_s']:.3f}s |",
        f"| Cleanup successes | {summary['cleanup_successes']} |",
    ]
    if summary.get("rerank_strategy"):
        lines.extend(
            [
                f"| Rerank strategy | {summary['rerank_strategy']} |",
                f"| Rerank pass rate | {summary['rerank_pass_rate']:.3f} |",
                f"| Rerank top-1 expected rate | {summary['rerank_top1_expected_rate']:.3f} |",
                f"| Rerank recency conflict pass rate | {summary['rerank_recency_conflict_pass_rate']:.3f} |",
                f"| Rerank distractor resistance pass rate | {summary['rerank_distractor_resistance_pass_rate']:.3f} |",
            ]
        )
    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Category | Pass | Reason |",
            "|---|---|---:|---|",
        ]
    )
    for row in rows:
        reason = []
        if not row["retrieved_expected"]:
            reason.append("missing expected")
        if row["forbidden_hit"]:
            reason.append("forbidden hit")
        if not row["top_result_ok"]:
            reason.append("top mismatch")
        pass_value = str(row["pass"])
        if "rerank_pass" in row:
            pass_value = f"{row['pass']} -> {row['rerank_pass']}"
        lines.append(f"| {row['id']} | {row['category']} | {pass_value} | {', '.join(reason) or 'ok'} |")
    lines.append("")
    return "\n".join(lines)


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=Path(__file__).resolve().parents[1] / "benchmarks" / "mem0_memory" / "smoke_suite.json")
    parser.add_argument("--tool", default="cmd", help="mem0 tool namespace to use for temporary benchmark memories")
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--keep-memories", action="store_true")
    parser.add_argument(
        "--rerank-strategy",
        choices=("vector", "score_plus_recency", "score_plus_created_at_rank", "benchmark_order"),
    )
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite = load_json(args.suite)
    if not isinstance(suite, list):
        raise ValueError(f"{args.suite}: expected JSON array")
    validate_suite(suite, args.suite)

    run_id = args.run_id or f"mem0-memory-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (resolve_default_output_root() / "mem0-memory-benchmark" / run_id)

    if args.dry_run:
        categories = Counter(str(case["category"]) for case in suite)
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"categories: {dict(categories)}")
        print(f"tool: {args.tool}")
        print(f"output_dir: {output_dir}")
        if args.rerank_strategy:
            print(f"rerank_strategy: {args.rerank_strategy}")
            print(f"recency_weight: {args.recency_weight}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    raw_rows: list[dict[str, Any]] = []
    add_latencies: list[float] = []
    search_latencies: list[float] = []
    added_ids: list[str] = []
    cleanup_successes = 0

    try:
        for index, case in enumerate(suite, 1):
            print(f"  [{index}/{len(suite)}] {case['category']} {case['id']}")
            case_ids: list[str] = []
            for memory_index, memory in enumerate(case["setup_memories"], 1):
                payload = cli_safe_text(f"[{run_id} {case['id']} m{memory_index}] {memory}")
                add_response, add_latency, raw_add = run_mem0([args.tool, "add", payload], args.timeout_s)
                add_latencies.append(add_latency)
                raw_rows.append({"id": case["id"], "operation": "add", "raw": raw_add})
                for result in add_response.get("results", []):
                    if isinstance(result, dict) and isinstance(result.get("id"), str):
                        added_ids.append(result["id"])
                        case_ids.append(result["id"])

            query = cli_safe_text(f"{case['query']} run id {run_id}")
            search_response, search_latency, raw_search = run_mem0([args.tool, "search", query], args.timeout_s)
            search_latencies.append(search_latency)
            raw_rows.append({"id": case["id"], "operation": "search", "raw": raw_search})
            search_result_objects = result_objects(search_response)
            memories = result_memories(search_response)
            scored = score_case(case, memories)
            row: dict[str, Any] = {
                "id": case["id"],
                "category": case["category"],
                "query": case["query"],
                "added_ids": case_ids,
                "search_latency_s": round(search_latency, 3),
                "results": memories,
                **scored,
            }
            if args.rerank_strategy:
                reranked = rerank_results(search_result_objects, args.rerank_strategy, args.recency_weight)
                reranked_memories = [str(item.get("memory") or "") for item in reranked]
                rerank_scored = score_case(case, reranked_memories)
                row.update(
                    {
                        "rerank_strategy": args.rerank_strategy,
                        "rerank_recency_weight": args.recency_weight,
                        "reranked_results": reranked_memories,
                        "rerank_top_result": rerank_scored["top_result"],
                        "rerank_pass": rerank_scored["pass"],
                        "rerank_retrieved_expected": rerank_scored["retrieved_expected"],
                        "rerank_forbidden_hit": rerank_scored["forbidden_hit"],
                        "rerank_top_result_ok": rerank_scored["top_result_ok"],
                    }
                )
            rows.append(row)
    finally:
        if not args.keep_memories:
            for memory_id in added_ids:
                try:
                    run_mem0([args.tool, "delete", memory_id], args.timeout_s)
                    cleanup_successes += 1
                except Exception as exc:  # pragma: no cover - cleanup best effort
                    print(f"warning: failed to delete memory {memory_id}: {exc}", file=sys.stderr)

    cases = len(rows)
    passed = sum(1 for row in rows if row["pass"])
    retrieved = sum(1 for row in rows if row["retrieved_expected"])
    top1 = sum(1 for row in rows if row["top_result_ok"])
    recency_rows = [row for row in rows if row["category"] == "recency_conflict"]
    distractor_rows = [row for row in rows if row["category"] == "distractor_resistance"]
    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "output_dir": str(output_dir),
        "tool": args.tool,
        "cases": cases,
        "passed": passed,
        "pass_rate": passed / max(1, cases),
        "recall_at_k": retrieved / max(1, cases),
        "top1_expected_rate": top1 / max(1, cases),
        "recency_conflict_pass_rate": sum(1 for row in recency_rows if row["pass"]) / max(1, len(recency_rows)),
        "distractor_resistance_pass_rate": sum(1 for row in distractor_rows if row["pass"]) / max(1, len(distractor_rows)),
        "add_latency_mean_s": statistics.fmean(add_latencies) if add_latencies else 0.0,
        "add_latency_p50_s": percentile(add_latencies, 0.50),
        "add_latency_p95_s": percentile(add_latencies, 0.95),
        "search_latency_mean_s": statistics.fmean(search_latencies) if search_latencies else 0.0,
        "search_latency_p50_s": percentile(search_latencies, 0.50),
        "search_latency_p95_s": percentile(search_latencies, 0.95),
        "cleanup_successes": cleanup_successes,
        "cleanup_expected": len(added_ids) if not args.keep_memories else 0,
        "kept_memories": args.keep_memories,
    }
    if args.rerank_strategy:
        rerank_passed = sum(1 for row in rows if row.get("rerank_pass"))
        rerank_top1 = sum(1 for row in rows if row.get("rerank_top_result_ok"))
        summary.update(
            {
                "rerank_strategy": args.rerank_strategy,
                "rerank_recency_weight": args.recency_weight,
                "rerank_passed": rerank_passed,
                "rerank_pass_rate": rerank_passed / max(1, cases),
                "rerank_top1_expected_rate": rerank_top1 / max(1, cases),
                "rerank_recency_conflict_pass_rate": sum(1 for row in recency_rows if row.get("rerank_pass"))
                / max(1, len(recency_rows)),
                "rerank_distractor_resistance_pass_rate": sum(
                    1 for row in distractor_rows if row.get("rerank_pass")
                )
                / max(1, len(distractor_rows)),
            }
        )

    save_jsonl(output_dir / "results.jsonl", rows)
    save_jsonl(output_dir / "raw_mem0_outputs.jsonl", raw_rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_summary_markdown(summary, rows), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"results: {output_dir / 'results.jsonl'}")
    print(f"summary: {output_dir / 'summary.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
