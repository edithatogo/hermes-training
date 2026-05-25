#!/usr/bin/env python3
"""Run an isolated mem0 add/search fixture and compare rerank strategies."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from mem0_rerank_lib import parse_mem0_search_output
    from mem0_rerank_search import rerank_search_results
    from run_fixed_reranking_benchmark import ndcg_at_k, percentile, reciprocal_rank
    from run_mem0_memory_benchmark import cli_safe_text, score_case, validate_suite
except ModuleNotFoundError:
    from scripts.mem0_rerank_lib import parse_mem0_search_output
    from scripts.mem0_rerank_search import rerank_search_results
    from scripts.run_fixed_reranking_benchmark import ndcg_at_k, percentile, reciprocal_rank
    from scripts.run_mem0_memory_benchmark import cli_safe_text, score_case, validate_suite


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


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


def safe_collection_suffix(run_id: str) -> str:
    suffix = re.sub(r"[^a-zA-Z0-9_]+", "_", run_id).strip("_").lower()
    return suffix[:64] or datetime.now(UTC).strftime("%Y%m%d_%H%M%S")


def write_fixture_config(base_config_path: Path, output_dir: Path, run_id: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    config = load_json(base_config_path)
    if not isinstance(config, dict):
        raise ValueError(f"{base_config_path}: expected object config")
    vector_store = dict(config.get("vector_store") or {})
    vector_config = dict(vector_store.get("config") or {})
    vector_config["collection_name"] = f"mem0_fixture_{safe_collection_suffix(run_id)}"
    vector_config["path"] = str(output_dir / "qdrant")
    vector_config["on_disk"] = True
    vector_store["provider"] = vector_store.get("provider") or "qdrant"
    vector_store["config"] = vector_config
    config["vector_store"] = vector_store
    config["history_db_path"] = str(output_dir / "history.db")
    config["fixture_run_id"] = run_id
    config_path = output_dir / "mem0-fixture-config.json"
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return config_path


def build_mem0_env(config_path: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["MEM0_CONFIG_PATH"] = str(config_path)
    return env


def run_mem0(args: list[str], timeout_s: float, env: dict[str, str]) -> tuple[str, float]:
    started = time.time()
    completed = subprocess.run(
        ["mem0", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
        check=False,
        env=env,
    )
    latency_s = time.time() - started
    if completed.returncode != 0:
        raise RuntimeError(f"mem0 {' '.join(args)} failed with {completed.returncode}:\n{completed.stdout}")
    return completed.stdout, latency_s


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


def added_memory_ids(add_response: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    results = add_response.get("results", [])
    if not isinstance(results, list):
        return ids
    for row in results:
        if isinstance(row, dict) and isinstance(row.get("id"), str):
            ids.append(row["id"])
    return ids


def annotate_relevance(case: dict[str, Any], results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected = [item.lower() for item in case["expected"]["must_retrieve_any"]]
    annotated: list[dict[str, Any]] = []
    for item in results:
        enriched = dict(item)
        memory = str(item.get("memory") or item.get("text") or "").lower()
        enriched["relevant"] = any(fragment in memory for fragment in expected)
        annotated.append(enriched)
    return annotated


def score_ranking(case: dict[str, Any], ranked: list[dict[str, Any]], latency_s: float) -> dict[str, Any]:
    memories = [str(item.get("memory") or item.get("text") or "") for item in ranked]
    scored = score_case(case, memories)
    return {
        "top_candidate_id": str(ranked[0].get("id", "")) if ranked else "",
        "top1_pass": scored["top_result_ok"],
        "pass": scored["pass"],
        "retrieved_expected": scored["retrieved_expected"],
        "forbidden_hit": scored["forbidden_hit"],
        "reciprocal_rank": reciprocal_rank(ranked),
        "ndcg_at_3": ndcg_at_k(ranked, 3),
        "recall_at_3": 1.0 if any(item.get("relevant") for item in ranked[:3]) else 0.0,
        "rerank_latency_s": round(latency_s, 6),
        "results": memories,
        "ranked_candidates": [
            {
                "id": str(item.get("id", "")),
                "memory": str(item.get("memory") or item.get("text") or ""),
                "base_score": round(float(item.get("base_score", item.get("score", 0.0)) or 0.0), 6),
                "rerank_score": round(float(item.get("rerank_score", item.get("score", 0.0)) or 0.0), 6),
            }
            for item in ranked
        ],
    }


def summarize_strategy(rows: list[dict[str, Any]], strategy: str) -> dict[str, Any]:
    strategy_rows = [row["strategies"][strategy] | {"category": row["category"]} for row in rows]
    cases = len(strategy_rows)
    recency_rows = [row for row in strategy_rows if row["category"] == "recency_conflict"]
    distractor_rows = [row for row in strategy_rows if row["category"] == "distractor_resistance"]
    latencies = [float(row["rerank_latency_s"]) for row in strategy_rows]
    return {
        "cases": cases,
        "pass_rate": sum(1 for row in strategy_rows if row["pass"]) / max(1, cases),
        "top1_accuracy": sum(1 for row in strategy_rows if row["top1_pass"]) / max(1, cases),
        "recall_at_3": statistics.fmean(row["recall_at_3"] for row in strategy_rows),
        "mrr": statistics.fmean(row["reciprocal_rank"] for row in strategy_rows),
        "ndcg_at_3": statistics.fmean(row["ndcg_at_3"] for row in strategy_rows),
        "recency_conflict_pass_rate": sum(1 for row in recency_rows if row["pass"]) / max(1, len(recency_rows)),
        "distractor_resistance_pass_rate": sum(1 for row in distractor_rows if row["pass"])
        / max(1, len(distractor_rows)),
        "rerank_latency_p50_s": percentile(latencies, 0.50),
        "rerank_latency_p95_s": percentile(latencies, 0.95),
    }


def render_summary_markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# mem0 Isolated Fixture Rerank: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        f"Fixture config: `{summary['fixture_config_path']}`",
        f"Collection: `{summary['collection_name']}`",
        "",
        "## Result",
        "",
        "| Strategy | Pass | Top-1 | Recall@3 | MRR | nDCG@3 | Recency conflict | Distractor resistance | p50 rerank |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for strategy, metrics in summary["strategies"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{strategy}`",
                    f"{metrics['pass_rate']:.3f}",
                    f"{metrics['top1_accuracy']:.3f}",
                    f"{metrics['recall_at_3']:.3f}",
                    f"{metrics['mrr']:.3f}",
                    f"{metrics['ndcg_at_3']:.3f}",
                    f"{metrics['recency_conflict_pass_rate']:.3f}",
                    f"{metrics['distractor_resistance_pass_rate']:.3f}",
                    f"{metrics['rerank_latency_p50_s']:.3f}s",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Category | Input count | " + " | ".join(summary["strategies"].keys()) + " |",
            "|---|---|---:|" + "---:|" * len(summary["strategies"]),
        ]
    )
    for row in rows:
        cells = [row["id"], row["category"], str(row["input_count"])]
        for strategy in summary["strategies"]:
            result = row["strategies"][strategy]
            cells.append(f"{result['top_candidate_id']} / {result['pass']}")
        lines.append("| " + " | ".join(cells) + " |")
    lines.extend(
        [
            "",
            "## Safety",
            "",
            "This run used `MEM0_CONFIG_PATH` and an output-local Qdrant path. It did not edit `~/.mem0/config.json` or the default `mem0_nomic_768` collection.",
            "",
        ]
    )
    return "\n".join(lines)


def preferred_summary_metrics(summary: dict[str, Any]) -> dict[str, Any]:
    strategies = summary.get("strategies", {})
    if not isinstance(strategies, dict) or not strategies:
        return {}
    ranked: list[tuple[tuple[float, float, float, int], str, dict[str, Any]]] = []
    for strategy, metrics in strategies.items():
        if not isinstance(metrics, dict):
            continue
        ranked.append(
            (
                (
                    float(metrics.get("top1_accuracy", 0.0) or 0.0),
                    float(metrics.get("pass_rate", 0.0) or 0.0),
                    float(metrics.get("mrr", 0.0) or 0.0),
                    1 if strategy.startswith("qwen3_causal_lm:") else 0,
                ),
                strategy,
                metrics,
            )
        )
    if not ranked:
        return {}
    _, strategy, metrics = max(ranked, key=lambda item: item[0])
    return metrics | {"strategy": strategy} if isinstance(metrics, dict) else {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=Path("benchmarks/mem0_memory/recency_suite.json"))
    parser.add_argument("--base-config", type=Path, default=Path.home() / ".mem0" / "config.json")
    parser.add_argument("--tool", default="cmd")
    parser.add_argument("--run-id", default=f"mem0-isolated-fixture-rerank-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument("--qwen3-model", default="Qwen/Qwen3-Reranker-0.6B")
    parser.add_argument("--qwen3-device", default="auto")
    parser.add_argument("--qwen3-max-length", type=int, default=4096)
    parser.add_argument("--qwen3-instruction", default="Retrieve memories that answer the query for a local Hermes agent.")
    parser.add_argument("--qwen3-local-files-only", action="store_true")
    parser.add_argument("--qwen3-server-url")
    parser.add_argument("--skip-qwen3", action="store_true")
    parser.add_argument("--keep-fixture", action="store_true", help="Keep output-local qdrant/history files after the run.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite = load_json(args.suite)
    if not isinstance(suite, list):
        raise ValueError(f"{args.suite}: expected JSON array")
    validate_suite(suite, args.suite)

    output_dir = args.output_dir or (resolve_default_output_root() / "mem0-isolated-fixture-rerank" / args.run_id)
    config_path = output_dir / "mem0-fixture-config.json"
    strategies: list[tuple[str, str | None]] = [
        ("vector", None),
        ("score_plus_created_at_rank_close_margin", None),
    ]
    if not args.skip_qwen3:
        strategies.append(("qwen3_causal_lm", args.qwen3_model))

    if args.dry_run:
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"base_config: {args.base_config}")
        print(f"fixture_config: {config_path}")
        print(f"output_dir: {output_dir}")
        print(f"strategies: {[strategy if model is None else f'{strategy}:{model}' for strategy, model in strategies]}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = write_fixture_config(args.base_config, output_dir, args.run_id)
    fixture_config = load_json(config_path)
    collection_name = fixture_config["vector_store"]["config"]["collection_name"]
    env = build_mem0_env(config_path)

    rows: list[dict[str, Any]] = []
    raw_rows: list[dict[str, Any]] = []
    add_latencies: list[float] = []
    search_latencies: list[float] = []
    added_ids: list[str] = []

    try:
        for index, case in enumerate(suite, 1):
            print(f"  [{index}/{len(suite)}] {case['category']} {case['id']}")
            case_ids: list[str] = []
            for memory_index, memory in enumerate(case["setup_memories"], 1):
                payload = cli_safe_text(f"[{args.run_id} {case['id']} m{memory_index}] {memory}")
                raw_add, add_latency_s = run_mem0([args.tool, "add", payload], args.timeout_s, env)
                add_latencies.append(add_latency_s)
                add_response = extract_first_json_object(raw_add)
                ids = added_memory_ids(add_response)
                added_ids.extend(ids)
                case_ids.extend(ids)
                raw_rows.append({"id": case["id"], "operation": "add", "raw": raw_add})

            query = cli_safe_text(f"{case['query']} run id {args.run_id}")
            raw_search, search_latency_s = run_mem0([args.tool, "search", query], args.timeout_s, env)
            search_latencies.append(search_latency_s)
            search_results = annotate_relevance(case, parse_mem0_search_output(raw_search))
            raw_rows.append({"id": case["id"], "operation": "search", "raw": raw_search})
            strategy_results: dict[str, Any] = {}
            for strategy, model in strategies:
                label = strategy if model is None else f"{strategy}:{model}"
                ranked, rerank_latency_s = rerank_search_results(
                    case["query"],
                    search_results,
                    strategy,
                    args.recency_weight,
                    model,
                    args.qwen3_device,
                    args.qwen3_max_length,
                    args.qwen3_instruction,
                    args.qwen3_local_files_only,
                    args.qwen3_server_url if strategy == "qwen3_causal_lm" else None,
                )
                strategy_results[label] = score_ranking(case, ranked, rerank_latency_s)
            rows.append(
                {
                    "id": case["id"],
                    "category": case["category"],
                    "query": case["query"],
                    "added_ids": case_ids,
                    "input_count": len(search_results),
                    "search_latency_s": round(search_latency_s, 3),
                    "raw_top_result": str(search_results[0].get("memory", "")) if search_results else "",
                    "strategies": strategy_results,
                }
            )
    finally:
        if not args.keep_fixture:
            shutil.rmtree(output_dir / "qdrant", ignore_errors=True)
            try:
                (output_dir / "history.db").unlink()
            except FileNotFoundError:
                pass

    summary = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "output_dir": str(output_dir),
        "tool": args.tool,
        "base_config_path": str(args.base_config),
        "fixture_config_path": str(config_path),
        "collection_name": collection_name,
        "fixture_qdrant_path": str(output_dir / "qdrant"),
        "kept_fixture": args.keep_fixture,
        "cases": len(rows),
        "add_latency_p50_s": percentile(add_latencies, 0.50),
        "add_latency_p95_s": percentile(add_latencies, 0.95),
        "search_latency_p50_s": percentile(search_latencies, 0.50),
        "search_latency_p95_s": percentile(search_latencies, 0.95),
        "input_count_min": min((row["input_count"] for row in rows), default=0),
        "input_count_max": max((row["input_count"] for row in rows), default=0),
        "added_memory_count": len(added_ids),
        "strategies": {strategy: summarize_strategy(rows, strategy) for strategy in rows[0]["strategies"]} if rows else {},
        "qwen3_device": args.qwen3_device,
        "qwen3_max_length": args.qwen3_max_length,
        "qwen3_server_url": args.qwen3_server_url or "",
        "qwen3_local_files_only": args.qwen3_local_files_only,
    }
    preferred = preferred_summary_metrics(summary)
    if preferred:
        summary.update(
            {
                "strategy": preferred["strategy"],
                "model": args.qwen3_model if preferred["strategy"].startswith("qwen3_causal_lm:") else "",
                "pass_rate": preferred["pass_rate"],
                "top1_accuracy": preferred["top1_accuracy"],
                "recall_at_3": preferred["recall_at_3"],
                "mrr": preferred["mrr"],
                "ndcg_at_3": preferred["ndcg_at_3"],
                "recency_conflict_pass_rate": preferred["recency_conflict_pass_rate"],
                "distractor_resistance_pass_rate": preferred["distractor_resistance_pass_rate"],
                "rerank_latency_p50_s": preferred["rerank_latency_p50_s"],
                "rerank_latency_p95_s": preferred["rerank_latency_p95_s"],
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
