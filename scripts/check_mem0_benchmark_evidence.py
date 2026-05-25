#!/usr/bin/env python3
"""Validate SSD-backed mem0 benchmark summary.json evidence."""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVAL_ROOT = Path(os.environ.get("HERMES_EVAL_ROOT", "/Volumes/PortableSSD/hermes-evals"))
DEFAULT_OUTPUT = ROOT / "reports" / "benchmark" / "mem0" / "validation" / "mem0-evidence-validation-20260526.json"

CORE_FIELDS = {"run_id", "created_at", "suite"}
RATE_FIELDS = {
    "pass_rate",
    "recall_at_k",
    "top1_expected_rate",
    "recency_conflict_pass_rate",
    "distractor_resistance_pass_rate",
    "rerank_pass_rate",
    "rerank_top1_expected_rate",
    "rerank_recency_conflict_pass_rate",
    "rerank_distractor_resistance_pass_rate",
    "top1_accuracy",
    "recall_at_3",
    "mrr",
    "ndcg_at_3",
    "json_validity_rate",
    "expected_extraction_rate",
    "forbidden_hit_rate",
    "empty_case_pass_rate",
}
LATENCY_FIELDS = {
    "add_latency_mean_s",
    "add_latency_p50_s",
    "add_latency_p95_s",
    "search_latency_mean_s",
    "search_latency_p50_s",
    "search_latency_p95_s",
    "embed_latency_mean_s",
    "embed_latency_p50_s",
    "embed_latency_p95_s",
    "latency_mean_s",
    "latency_p50_s",
    "latency_p95_s",
    "rerank_latency_mean_s",
    "rerank_latency_p50_s",
    "rerank_latency_p95_s",
    "elapsed_s",
}


@dataclass(frozen=True)
class EvidenceSource:
    kind: str
    glob: str


SOURCES = (
    EvidenceSource("memory", "mem0-memory-benchmark/**/summary.json"),
    EvidenceSource("embedding", "embedding-benchmark/**/summary.json"),
    EvidenceSource("extraction", "mem0-extraction-benchmark/**/summary.json"),
    EvidenceSource("reranking", "mem0-reranking-benchmark/**/summary.json"),
    EvidenceSource("replay", "mem0-reranking-replay/**/summary.json"),
    EvidenceSource("isolated-fixture", "mem0-isolated-fixture-rerank/**/summary.json"),
)


def load_summary(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def missing(summary: dict[str, Any], fields: set[str]) -> list[str]:
    return sorted(field for field in fields if field not in summary)


def is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def validate_common(summary: dict[str, Any]) -> list[str]:
    errors = [f"missing {field}" for field in missing(summary, CORE_FIELDS)]
    for field in RATE_FIELDS & summary.keys():
        value = summary[field]
        if not is_number(value) or not 0 <= float(value) <= 1:
            errors.append(f"{field} must be numeric in [0, 1]")
    for field in LATENCY_FIELDS & summary.keys():
        value = summary[field]
        if not is_number(value) or float(value) < 0:
            errors.append(f"{field} must be non-negative numeric")
    for field in ("cases", "passed", "cleanup_successes", "cleanup_expected", "input_count_min", "input_count_max", "added_memory_count"):
        if field in summary and (not isinstance(summary[field], int) or isinstance(summary[field], bool) or summary[field] < 0):
            errors.append(f"{field} must be a non-negative integer")
    if "kept_memories" in summary and not isinstance(summary["kept_memories"], bool):
        errors.append("kept_memories must be boolean")
    return errors


def validate_memory(path: Path, summary: dict[str, Any]) -> list[str]:
    if "/rerank/" in path.as_posix():
        required = {
            "run_id",
            "created_at",
            "source_run_dir",
            "suite",
            "strategy",
            "recency_weight",
            "cases",
            "passed",
            "pass_rate",
            "top1_expected_rate",
            "recency_conflict_pass_rate",
            "distractor_resistance_pass_rate",
        }
    else:
        required = {
            "run_id",
            "created_at",
            "suite",
            "output_dir",
            "tool",
            "cases",
            "passed",
            "pass_rate",
            "recall_at_k",
            "top1_expected_rate",
            "recency_conflict_pass_rate",
            "distractor_resistance_pass_rate",
            "add_latency_mean_s",
            "add_latency_p50_s",
            "add_latency_p95_s",
            "search_latency_mean_s",
            "search_latency_p50_s",
            "search_latency_p95_s",
            "cleanup_successes",
            "cleanup_expected",
            "kept_memories",
        }
    return [f"missing {field}" for field in missing(summary, required)]


def validate_embedding(summary: dict[str, Any]) -> list[str]:
    required = {
        "run_id",
        "created_at",
        "suite",
        "output_dir",
        "model",
        "cases",
        "top1_accuracy",
        "recall_at_3",
        "mrr",
        "ndcg_at_3",
        "embedding_dims",
        "embed_latency_mean_s",
        "embed_latency_p50_s",
        "embed_latency_p95_s",
    }
    errors = [f"missing {field}" for field in missing(summary, required)]
    dims = summary.get("embedding_dims")
    if dims is not None and (not isinstance(dims, int) or isinstance(dims, bool) or dims <= 0):
        errors.append("embedding_dims must be a positive integer")
    return errors


def validate_extraction(summary: dict[str, Any]) -> list[str]:
    required = {
        "run_id",
        "created_at",
        "suite",
        "output_dir",
        "model",
        "base_url",
        "cases",
        "passed",
        "pass_rate",
        "json_validity_rate",
        "expected_extraction_rate",
        "forbidden_hit_rate",
        "empty_case_pass_rate",
        "latency_mean_s",
        "latency_p50_s",
        "latency_p95_s",
    }
    return [f"missing {field}" for field in missing(summary, required)]


def validate_reranking(summary: dict[str, Any]) -> list[str]:
    if summary.get("status") == "blocked":
        required = {
            "run_id",
            "created_at",
            "status",
            "suite",
            "output_dir",
            "model",
            "blocker",
            "elapsed_s",
            "runtime",
            "npm_package",
            "device",
            "dtype",
            "max_length",
            "limit_cases",
            "tool_root",
            "cache_root",
            "cases",
        }
        return [f"missing {field}" for field in missing(summary, required)]

    required = {
        "run_id",
        "created_at",
        "suite",
        "output_dir",
        "model",
        "cases",
        "top1_accuracy",
        "recall_at_3",
        "mrr",
        "ndcg_at_3",
        "recency_conflict_pass_rate",
        "distractor_resistance_pass_rate",
        "rerank_latency_p50_s",
        "rerank_latency_p95_s",
    }
    return [f"missing {field}" for field in missing(summary, required)]


def validate_replay(summary: dict[str, Any]) -> list[str]:
    required = {
        "run_id",
        "created_at",
        "suite",
        "output_dir",
        "model",
        "strategy",
        "recency_weight",
        "cases",
        "top1_accuracy",
        "recall_at_3",
        "mrr",
        "ndcg_at_3",
        "recency_conflict_pass_rate",
        "distractor_resistance_pass_rate",
        "rerank_latency_mean_s",
        "rerank_latency_p50_s",
        "rerank_latency_p95_s",
        "qwen3_device",
        "qwen3_instruction",
        "qwen3_local_files_only",
        "qwen3_max_length",
        "qwen3_server_url",
    }
    return [f"missing {field}" for field in missing(summary, required)]


def validate_isolated_fixture(summary: dict[str, Any]) -> list[str]:
    required = {
        "run_id",
        "created_at",
        "suite",
        "output_dir",
        "tool",
        "base_config_path",
        "fixture_config_path",
        "collection_name",
        "fixture_qdrant_path",
        "kept_fixture",
        "cases",
        "add_latency_p50_s",
        "add_latency_p95_s",
        "search_latency_p50_s",
        "search_latency_p95_s",
        "input_count_min",
        "input_count_max",
        "added_memory_count",
        "strategies",
        "qwen3_local_files_only",
        "qwen3_server_url",
        "strategy",
        "model",
        "pass_rate",
        "top1_accuracy",
        "recall_at_3",
        "mrr",
        "ndcg_at_3",
        "recency_conflict_pass_rate",
        "distractor_resistance_pass_rate",
        "rerank_latency_p50_s",
        "rerank_latency_p95_s",
    }
    errors = [f"missing {field}" for field in missing(summary, required)]
    strategies = summary.get("strategies")
    if not isinstance(strategies, dict) or not strategies:
        errors.append("strategies must be a non-empty object")
        return errors
    strategy_name = summary.get("strategy")
    if strategy_name not in strategies:
        errors.append("strategy must select an entry from strategies")
        return errors
    required_strategy = {
        "cases",
        "pass_rate",
        "top1_accuracy",
        "recall_at_3",
        "mrr",
        "ndcg_at_3",
        "recency_conflict_pass_rate",
        "distractor_resistance_pass_rate",
        "rerank_latency_p50_s",
        "rerank_latency_p95_s",
    }
    for name, value in strategies.items():
        if not isinstance(value, dict):
            errors.append(f"strategies.{name} must be an object")
            continue
        errors.extend(f"strategies.{name} missing {field}" for field in missing(value, required_strategy))
    selected = strategies.get(strategy_name, {})
    for field in required_strategy - {"cases"}:
        if field in summary and field in selected and summary[field] != selected[field]:
            errors.append(f"{field} does not match selected strategy {strategy_name}")
    return errors


VALIDATORS = {
    "memory": validate_memory,
    "embedding": lambda path, summary: validate_embedding(summary),
    "extraction": lambda path, summary: validate_extraction(summary),
    "reranking": lambda path, summary: validate_reranking(summary),
    "replay": lambda path, summary: validate_replay(summary),
    "isolated-fixture": lambda path, summary: validate_isolated_fixture(summary),
}


def validate_file(kind: str, path: Path, eval_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    try:
        summary = load_summary(path)
    except Exception as exc:  # noqa: BLE001
        return {"kind": kind, "path": str(path), "status": "failed", "errors": [str(exc)]}
    errors.extend(validate_common(summary))
    errors.extend(VALIDATORS[kind](path, summary))
    return {
        "kind": kind,
        "path": str(path.relative_to(eval_root)) if path.is_relative_to(eval_root) else str(path),
        "run_id": summary.get("run_id", ""),
        "status": "passed" if not errors else "failed",
        "errors": errors,
    }


def build_report(eval_root: Path) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for source in SOURCES:
        for path in sorted(eval_root.glob(source.glob)):
            items.append(validate_file(source.kind, path, eval_root))
    counts: dict[str, int] = {}
    by_kind: dict[str, int] = {}
    for item in items:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
        by_kind[item["kind"]] = by_kind.get(item["kind"], 0) + 1
    missing_kinds = [source.kind for source in SOURCES if by_kind.get(source.kind, 0) == 0]
    status = "passed" if items and counts.get("failed", 0) == 0 and not missing_kinds else "failed"
    return {
        "created_at": datetime.now(UTC).isoformat(),
        "eval_root": str(eval_root),
        "status": status,
        "counts": counts,
        "by_kind": by_kind,
        "missing_kinds": missing_kinds,
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-root", type=Path, default=DEFAULT_EVAL_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    report = build_report(args.eval_root)
    if not args.no_write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "counts", "by_kind", "missing_kinds")}, indent=2))
    if report["status"] != "passed":
        for item in report["items"]:
            if item["status"] == "failed":
                print(f"{item['path']}: {', '.join(item['errors'])}", file=sys.stderr)
        for kind in report["missing_kinds"]:
            print(f"missing mem0 evidence kind: {kind}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
