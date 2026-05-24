#!/usr/bin/env python3
"""Evaluate offline reranking strategies over a saved mem0 benchmark run."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{lineno}: row must be an object")
            rows.append(row)
    return rows


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
    raise ValueError(f"raw mem0 output did not contain a JSON object: {text[:500]}")


def parse_timestamp(value: str | None) -> float:
    if not value:
        return 0.0
    try:
        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).timestamp()
    except ValueError:
        return 0.0


def score_expected(case: dict[str, Any], memories: list[str]) -> dict[str, Any]:
    joined = "\n".join(memories).lower()
    top = memories[0].lower() if memories else ""
    expected = case["expected"]
    must_any = [item.lower() for item in expected["must_retrieve_any"]]
    must_not = [item.lower() for item in expected.get("must_not_retrieve_any", [])]
    top_contains = expected.get("top_result_should_contain")

    retrieved = any(item in joined for item in must_any)
    forbidden_hit = any(item in joined for item in must_not)
    top_ok = True if not top_contains else top_contains.lower() in top
    return {
        "pass": retrieved and not forbidden_hit and top_ok,
        "retrieved_expected": retrieved,
        "forbidden_hit": forbidden_hit,
        "top_result_ok": top_ok,
        "top_result": memories[0] if memories else "",
    }


def load_suite_by_id(path: Path) -> dict[str, dict[str, Any]]:
    suite = load_json(path)
    if not isinstance(suite, list):
        raise ValueError(f"{path}: expected a JSON array")
    return {str(case["id"]): case for case in suite if isinstance(case, dict) and "id" in case}


def search_rows_by_case(raw_rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_case: dict[str, list[dict[str, Any]]] = {}
    for row in raw_rows:
        if row.get("operation") != "search":
            continue
        case_id = row.get("id")
        raw = row.get("raw")
        if not isinstance(case_id, str) or not isinstance(raw, str):
            continue
        parsed = extract_first_json_object(raw)
        results = parsed.get("results", [])
        if isinstance(results, list):
            by_case[case_id] = [item for item in results if isinstance(item, dict)]
    return by_case


def benchmark_memory_index(memory: str) -> int | None:
    match = re.search(r"\sm(\d+)\]", memory)
    if not match:
        return None
    return int(match.group(1))


def rerank_results(results: list[dict[str, Any]], strategy: str, recency_weight: float) -> list[dict[str, Any]]:
    if strategy == "vector":
        return sorted(results, key=lambda item: float(item.get("score") or 0.0), reverse=True)

    timestamps = [parse_timestamp(item.get("created_at")) for item in results]
    newest = max(timestamps) if timestamps else 0.0
    oldest = min(timestamps) if timestamps else 0.0
    span = max(1.0, newest - oldest)
    timestamp_order = {
        id(item): rank
        for rank, item in enumerate(
            sorted(results, key=lambda candidate: parse_timestamp(candidate.get("created_at"))),
            1,
        )
    }

    ranked: list[dict[str, Any]] = []
    for item in results:
        base_score = float(item.get("score") or 0.0)
        created_at = parse_timestamp(item.get("created_at"))
        recency_score = (created_at - oldest) / span if created_at else 0.0
        adjusted = base_score
        if strategy == "score_plus_recency":
            adjusted = base_score + recency_weight * recency_score
        elif strategy == "score_plus_created_at_rank":
            rank_score = timestamp_order.get(id(item), 0) / max(1, len(results))
            adjusted = base_score + recency_weight * rank_score
        elif strategy == "benchmark_order":
            memory = str(item.get("memory") or "")
            index = benchmark_memory_index(memory) or 0
            adjusted = base_score + recency_weight * math.log1p(index)
        else:
            raise ValueError(f"unsupported strategy {strategy}")
        enriched = dict(item)
        enriched["base_score"] = base_score
        enriched["recency_score"] = recency_score
        enriched["rerank_score"] = adjusted
        ranked.append(enriched)
    return sorted(ranked, key=lambda item: float(item["rerank_score"]), reverse=True)


def render_summary_markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# mem0 Reranking Evaluation: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Cases | {summary['cases']} |",
        f"| Strategy | {summary['strategy']} |",
        f"| Recency weight | {summary['recency_weight']:.3f} |",
        f"| Pass rate | {summary['pass_rate']:.3f} |",
        f"| Top-1 expected rate | {summary['top1_expected_rate']:.3f} |",
        f"| Recency conflict pass rate | {summary['recency_conflict_pass_rate']:.3f} |",
        f"| Distractor resistance pass rate | {summary['distractor_resistance_pass_rate']:.3f} |",
        "",
        "## Cases",
        "",
        "| Case | Category | Top result | Pass |",
        "|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['id']} | {row['category']} | {row['top_result_id']} | {row['pass']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=Path(__file__).resolve().parents[1] / "benchmarks" / "mem0_memory" / "smoke_suite.json")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument(
        "--strategy",
        choices=("vector", "score_plus_recency", "score_plus_created_at_rank", "benchmark_order"),
        default="score_plus_recency",
    )
    parser.add_argument("--recency-weight", type=float, default=0.05)
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    suite_by_id = load_suite_by_id(args.suite)
    raw_rows = load_jsonl(args.run_dir / "raw_mem0_outputs.jsonl")
    searches = search_rows_by_case(raw_rows)

    run_id = args.run_id or f"mem0-rerank-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (args.run_dir / "rerank" / run_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for case_id, case in suite_by_id.items():
        results = searches.get(case_id, [])
        ranked = rerank_results(results, args.strategy, args.recency_weight)
        memories = [str(item.get("memory") or "") for item in ranked]
        scored = score_expected(case, memories)
        rows.append(
            {
                "id": case_id,
                "category": case["category"],
                "top_result_id": str(ranked[0].get("id")) if ranked else "",
                "top_result_memory": memories[0] if memories else "",
                "ranked": [
                    {
                        "id": item.get("id"),
                        "score": item.get("score"),
                        "rerank_score": round(float(item.get("rerank_score") or 0.0), 6),
                        "created_at": item.get("created_at"),
                        "memory": item.get("memory"),
                    }
                    for item in ranked
                ],
                **scored,
            }
        )

    cases = len(rows)
    recency_rows = [row for row in rows if row["category"] == "recency_conflict"]
    distractor_rows = [row for row in rows if row["category"] == "distractor_resistance"]
    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "source_run_dir": str(args.run_dir),
        "suite": str(args.suite),
        "strategy": args.strategy,
        "recency_weight": args.recency_weight,
        "cases": cases,
        "passed": sum(1 for row in rows if row["pass"]),
        "pass_rate": sum(1 for row in rows if row["pass"]) / max(1, cases),
        "top1_expected_rate": sum(1 for row in rows if row["top_result_ok"]) / max(1, cases),
        "recency_conflict_pass_rate": sum(1 for row in recency_rows if row["pass"]) / max(1, len(recency_rows)),
        "distractor_resistance_pass_rate": sum(1 for row in distractor_rows if row["pass"]) / max(1, len(distractor_rows)),
    }
    save_jsonl(output_dir / "results.jsonl", rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_summary_markdown(summary, rows), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"results: {output_dir / 'results.jsonl'}")
    print(f"summary: {output_dir / 'summary.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
