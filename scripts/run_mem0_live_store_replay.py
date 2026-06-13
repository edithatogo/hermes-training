#!/usr/bin/env python3
"""Replay a bounded copy of live mem0 memories into an EmbeddingGemma profile."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import site
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from render_mem0_embeddinggemma_config import DEFAULT_BASE_URL, DEFAULT_DIMS, DEFAULT_MODEL, render_config
except ModuleNotFoundError:
    from scripts.render_mem0_embeddinggemma_config import DEFAULT_BASE_URL, DEFAULT_DIMS, DEFAULT_MODEL, render_config


DEFAULT_QUERIES = (
    "Hermes current recommended strict tool-call adapter",
    "mem0 default rollback embedder and collection",
    "EmbeddingGemma candidate collection and promotion status",
    "Qwen3 v6 publication gate status",
    "Azure or Colab backend priority for bounded benchmarks",
)

HELPER = r"""
import json
import os
import site
import sys

mem0_dir = os.path.expanduser("~/.mem0")
if mem0_dir not in sys.path:
    sys.path.insert(0, mem0_dir)
user_site = site.getusersitepackages()
if user_site and user_site not in sys.path:
    sys.path.append(user_site)

from mem0_wrapper import add_memory, search_memory  # type: ignore

op = sys.argv[1]
if op == "search":
    query = sys.argv[2]
    limit = int(sys.argv[3])
    user_id = sys.argv[4] or None
    agent_id = sys.argv[5] or None
    result = search_memory(query, user_id=user_id, agent_id=agent_id, limit=limit)
elif op == "add":
    memory = sys.argv[2]
    user_id = sys.argv[3]
    agent_id = sys.argv[4]
    metadata = json.loads(sys.argv[5])
    result = add_memory(memory, user_id=user_id, agent_id=agent_id, metadata=metadata, infer=False)
else:
    raise SystemExit(f"unsupported op {op}")

print(json.dumps(result, ensure_ascii=False))
"""


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:80] or "run"


def resolve_eval_root() -> Path:
    if os.environ.get("HERMES_EVAL_ROOT"):
        return Path(os.environ["HERMES_EVAL_ROOT"])
    if os.environ.get("HERMES_STORAGE_ROOT"):
        return Path(os.environ["HERMES_STORAGE_ROOT"]) / "hermes-evals"
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD") / "hermes-evals"
    return Path.cwd() / ".local-storage" / "hermes-evals"


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def normalize_results(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, dict) and isinstance(raw.get("results"), list):
        return [item for item in raw["results"] if isinstance(item, dict)]
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    return []


def memory_text(item: dict[str, Any]) -> str:
    for key in ("memory", "text", "content"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return json.dumps(item, sort_keys=True, ensure_ascii=False)


def text_hash(text: str) -> str:
    normalized = " ".join(text.strip().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def result_hash(item: dict[str, Any]) -> str:
    metadata = item.get("metadata")
    if isinstance(metadata, dict):
        value = metadata.get("source_hash")
        if isinstance(value, str) and value:
            return value
    return text_hash(memory_text(item))


def short_hash(value: str) -> str:
    return value[:12]


def redacted_result(item: dict[str, Any], rank: int) -> dict[str, Any]:
    text = memory_text(item)
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    return {
        "rank": rank,
        "hash": text_hash(text),
        "source_hash": metadata.get("source_hash") if isinstance(metadata, dict) else "",
        "chars": len(text),
        "score": item.get("score"),
        "created_at_present": bool(item.get("created_at")),
        "metadata_keys": sorted(metadata.keys()) if isinstance(metadata, dict) else [],
    }


def subprocess_env(config_path: Path | None) -> dict[str, str]:
    env = os.environ.copy()
    if config_path:
        env["MEM0_CONFIG_PATH"] = str(config_path)
    else:
        env.pop("MEM0_CONFIG_PATH", None)
    path_parts = pythonpath_parts()
    path_parts.insert(0, str(Path.home() / ".mem0"))
    user_site = site.getusersitepackages()
    if user_site:
        path_parts.append(user_site)
    if env.get("PYTHONPATH"):
        path_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(path_parts)
    return env


def pythonpath_parts() -> list[str]:
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    candidates = [
        Path.home() / "Library" / "Python" / current_version / "lib" / "python" / "site-packages",
        *sorted(Path("/opt/homebrew/lib").glob(f"python{current_version}/site-packages")),
    ]
    return [str(path) for path in candidates if path.exists()]


def run_helper(
    op: str,
    args: list[str],
    *,
    config_path: Path | None,
    timeout_s: float,
) -> Any:
    completed = subprocess.run(
        [sys.executable, "-c", HELPER, op, *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=subprocess_env(config_path),
        timeout=timeout_s,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"mem0 helper {op} failed with {completed.returncode}:\n{completed.stderr}\n{completed.stdout}")
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError(f"mem0 helper {op} produced no JSON")
    return json.loads(lines[-1])


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def render_candidate_config(
    *,
    base_config_path: Path,
    output_dir: Path,
    collection_name: str,
    base_url: str,
    model: str,
    dims: int,
) -> Path:
    config = render_config(
        load_json(base_config_path),
        collection_name=collection_name,
        qdrant_path=output_dir / "qdrant",
        history_db_path=output_dir / "history.db",
        base_url=base_url,
        model=model,
        dims=dims,
        api_key="local-live-replay",
    )
    config_path = output_dir / "candidate-config.json"
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return config_path


def compare_case(
    query_id: str,
    default_results: list[dict[str, Any]],
    candidate_results: list[dict[str, Any]],
) -> dict[str, Any]:
    default_hashes = [result_hash(item) for item in default_results]
    candidate_hashes = [result_hash(item) for item in candidate_results]
    default_top = default_hashes[0] if default_hashes else ""
    candidate_top = candidate_hashes[0] if candidate_hashes else ""
    return {
        "query_id": query_id,
        "default_count": len(default_results),
        "candidate_count": len(candidate_results),
        "default_top_hash": default_top,
        "candidate_top_hash": candidate_top,
        "top1_match": bool(default_top and default_top == candidate_top),
        "default_top_recall_at_candidate_k": bool(default_top and default_top in candidate_hashes),
        "overlap_at_candidate_k": len(set(default_hashes).intersection(candidate_hashes)),
    }


def aggregate(cases: list[dict[str, Any]]) -> dict[str, Any]:
    comparable = [case for case in cases if case["default_count"] > 0]
    if not comparable:
        return {
            "comparable_cases": 0,
            "top1_match_rate": 0.0,
            "default_top_recall_rate": 0.0,
            "mean_overlap_at_k": 0.0,
        }
    return {
        "comparable_cases": len(comparable),
        "top1_match_rate": sum(1 for case in comparable if case["top1_match"]) / len(comparable),
        "default_top_recall_rate": sum(1 for case in comparable if case["default_top_recall_at_candidate_k"]) / len(comparable),
        "mean_overlap_at_k": sum(float(case["overlap_at_candidate_k"]) for case in comparable) / len(comparable),
    }


def render_report(summary: dict[str, Any]) -> str:
    metrics = summary["metrics"]
    lines = [
        "# EmbeddingGemma Copied Live-Store Replay",
        "",
        f"Run ID: `{summary['run_id']}`",
        f"Created: `{summary['created_at']}`",
        "",
        "## Scope",
        "",
        "This report compares a bounded, copied sample from the current default mem0 store against an",
        "EmbeddingGemma candidate collection. Raw memory text is not committed; private raw artifacts",
        "remain on the SSD path listed below.",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Queries | {summary['query_count']} |",
        f"| Unique copied memories | {summary['unique_memory_count']} |",
        f"| Comparable cases | {metrics['comparable_cases']} |",
        f"| Top-1 match rate | {metrics['top1_match_rate']:.3f} |",
        f"| Default top recall@candidate-k | {metrics['default_top_recall_rate']:.3f} |",
        f"| Mean overlap@candidate-k | {metrics['mean_overlap_at_k']:.3f} |",
        "",
        "## Default Filter",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| user_id | `{summary.get('default_user_id', '')}` |",
        f"| agent_id | `{summary.get('default_agent_id', '')}` |",
        "",
        "## Redacted Case Results",
        "",
        "| Query ID | Default count | Candidate count | Top-1 match | Recall | Default top hash | Candidate top hash |",
        "|---|---:|---:|---|---|---|---|",
    ]
    for case in summary["cases"]:
        lines.append(
            "| {query_id} | {default_count} | {candidate_count} | {top1_match} | {default_top_recall_at_candidate_k} | `{default_hash}` | `{candidate_hash}` |".format(
                query_id=case["query_id"],
                default_count=case["default_count"],
                candidate_count=case["candidate_count"],
                top1_match="yes" if case["top1_match"] else "no",
                default_top_recall_at_candidate_k="yes" if case["default_top_recall_at_candidate_k"] else "no",
                default_hash=short_hash(str(case["default_top_hash"])),
                candidate_hash=short_hash(str(case["candidate_top_hash"])),
            )
        )
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            f"- Private raw export: `{summary['private_raw_export_path']}`",
            f"- Private raw candidate search: `{summary['private_candidate_search_path']}`",
            f"- Redacted summary JSON: `{summary['summary_json_path']}`",
            f"- Candidate config: `{summary['candidate_config_path']}`",
            f"- Candidate collection: `{summary['candidate_collection']}`",
            "",
            "## Decision",
            "",
            summary["decision"],
            "",
            "## Rollback",
            "",
            "No live default config was edited. Rollback remains `unset MEM0_CONFIG_PATH` and the",
            "current `nomic-embed-text:latest` / `mem0_nomic_768` default path.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    run_id = f"embeddinggemma-live-store-replay-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=run_id)
    parser.add_argument("--query", action="append", default=[])
    parser.add_argument("--default-limit", type=int, default=3)
    parser.add_argument("--candidate-limit", type=int, default=5)
    parser.add_argument("--default-user-id", default="default_user")
    parser.add_argument("--default-agent-id", default="")
    parser.add_argument("--timeout-s", type=float, default=180.0)
    parser.add_argument("--base-config", type=Path, default=Path.home() / ".mem0" / "config.json")
    parser.add_argument("--output-root", type=Path, default=resolve_eval_root() / "mem0-live-store-replay")
    parser.add_argument("--collection-name")
    parser.add_argument("--embedding-base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--embedding-model", default=DEFAULT_MODEL)
    parser.add_argument("--embedding-dims", type=int, default=DEFAULT_DIMS)
    parser.add_argument("--report-output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.default_limit <= 0 or args.candidate_limit <= 0:
        raise SystemExit("limits must be > 0")
    queries = args.query or list(DEFAULT_QUERIES)
    output_dir = args.output_root / args.run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    collection = args.collection_name or f"mem0_embeddinggemma_300m_768_{slugify(args.run_id)}"
    config_path = render_candidate_config(
        base_config_path=args.base_config,
        output_dir=output_dir,
        collection_name=collection,
        base_url=args.embedding_base_url,
        model=args.embedding_model,
        dims=args.embedding_dims,
    )

    default_rows: list[dict[str, Any]] = []
    unique_memories: dict[str, str] = {}
    started = time.perf_counter()
    for index, query in enumerate(queries, 1):
        query_id = f"q{index:02d}-{slugify(query)[:40]}"
        raw = run_helper(
            "search",
            [query, str(args.default_limit), args.default_user_id, args.default_agent_id],
            config_path=None,
            timeout_s=args.timeout_s,
        )
        results = normalize_results(raw)
        for rank, item in enumerate(results, 1):
            text = memory_text(item)
            h = text_hash(text)
            unique_memories.setdefault(h, text)
            default_rows.append(
                {
                    "query_id": query_id,
                    "query": query,
                    "rank": rank,
                    "hash": h,
                    "raw": item,
                }
            )

    user_id = f"live_replay_{slugify(args.run_id)}"
    agent_id = "embeddinggemma_live_store_replay"
    for index, (source_hash, text) in enumerate(unique_memories.items(), 1):
        metadata = {
            "source": "copied_live_store_replay",
            "run_id": args.run_id,
            "source_hash": source_hash,
            "copy_index": index,
        }
        run_helper(
            "add",
            [text, user_id, agent_id, json.dumps(metadata, ensure_ascii=False)],
            config_path=config_path,
            timeout_s=args.timeout_s,
        )

    candidate_rows: list[dict[str, Any]] = []
    cases: list[dict[str, Any]] = []
    for index, query in enumerate(queries, 1):
        query_id = f"q{index:02d}-{slugify(query)[:40]}"
        default_results = [row["raw"] for row in default_rows if row["query_id"] == query_id]
        raw = run_helper(
            "search",
            [query, str(args.candidate_limit), user_id, agent_id],
            config_path=config_path,
            timeout_s=args.timeout_s,
        )
        candidate_results = normalize_results(raw)
        for rank, item in enumerate(candidate_results, 1):
            candidate_rows.append(
                {
                    "query_id": query_id,
                    "query": query,
                    "rank": rank,
                    "hash": result_hash(item),
                    "raw": item,
                }
            )
        cases.append(compare_case(query_id, default_results, candidate_results))

    private_default_path = output_dir / "private-default-search-results.jsonl"
    private_candidate_path = output_dir / "private-candidate-search-results.jsonl"
    write_jsonl(private_default_path, default_rows)
    write_jsonl(private_candidate_path, candidate_rows)

    metrics = aggregate(cases)
    decision = (
        "EmbeddingGemma matched the current default top memory for every comparable copied-live-store query. "
        "It remains non-default until the user approves a live config switch and rollback smoke."
        if metrics["comparable_cases"] and metrics["top1_match_rate"] == 1.0
        else "EmbeddingGemma did not fully match the current default on the copied-live-store replay; keep it opt-in."
    )
    summary = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "query_count": len(queries),
        "unique_memory_count": len(unique_memories),
        "candidate_collection": collection,
        "default_user_id": args.default_user_id,
        "default_agent_id": args.default_agent_id,
        "candidate_config_path": str(config_path),
        "private_raw_export_path": str(private_default_path),
        "private_candidate_search_path": str(private_candidate_path),
        "summary_json_path": str(output_dir / "summary-redacted.json"),
        "metrics": metrics,
        "cases": cases,
        "redacted_default_results": [redacted_result(row["raw"], int(row["rank"])) for row in default_rows],
        "redacted_candidate_results": [redacted_result(row["raw"], int(row["rank"])) for row in candidate_rows],
        "elapsed_s": round(time.perf_counter() - started, 3),
        "decision": decision,
    }
    summary_path = output_dir / "summary-redacted.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = render_report(summary)
    report_path = args.report_output or output_dir / "report-redacted.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    print(json.dumps({"status": "passed", "summary": str(summary_path), "report": str(report_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
