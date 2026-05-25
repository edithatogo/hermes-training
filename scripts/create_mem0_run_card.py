#!/usr/bin/env python3
"""Create a mem0 run card from a benchmark summary.json."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def infer_kind(path: Path, summary: dict[str, Any]) -> str:
    text = str(path)
    if "mem0-reranking-benchmark" in text:
        return "reranking"
    if "embedding-benchmark" in text:
        return "embedding"
    if "mem0-extraction-benchmark" in text:
        return "extraction"
    if "mem0-memory-benchmark" in text and summary.get("rerank_strategy"):
        return "memory+rerank"
    if "mem0-memory-benchmark" in text:
        return "memory"
    if summary.get("endpoint_kind") == "openai-compatible-embeddings":
        return "embedding"
    if "json_validity_rate" in summary:
        return "extraction"
    if "top1_accuracy" in summary:
        return "embedding"
    return "memory"


def format_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def metric(summary: dict[str, Any], *names: str) -> str:
    for name in names:
        if name in summary:
            return format_value(summary[name])
    return ""


def command_for_kind(kind: str, summary: dict[str, Any]) -> list[str]:
    suite = summary.get("suite", "<suite>")
    run_id = summary.get("run_id", "<run-id>")
    if kind == "embedding":
        endpoint_kind = summary.get("endpoint_kind")
        if endpoint_kind == "openai-compatible-embeddings":
            script = "scripts/run_openai_embedding_benchmark.py"
        elif endpoint_kind == "sentence-transformers":
            script = "scripts/run_sentence_transformers_embedding_benchmark.py"
        else:
            script = "scripts/run_ollama_embedding_benchmark.py"
        lines = [
            f"./.venv/bin/python {script} \\",
            f"  --model {summary.get('model', '<model>')} \\",
        ]
        if script == "scripts/run_sentence_transformers_embedding_benchmark.py" and summary.get("device"):
            lines.append(f"  --device {summary['device']} \\")
        if script == "scripts/run_openai_embedding_benchmark.py" and summary.get("base_url"):
            lines.append(f"  --base-url {summary['base_url']} \\")
        lines.extend([f"  --suite {suite} \\", f"  --run-id {run_id}"])
        return lines
    if kind == "extraction":
        lines = [
            "./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \\",
            f"  --model {summary.get('model', '<model>')} \\",
        ]
        if summary.get("base_url"):
            lines.append(f"  --base-url {summary['base_url']} \\")
        lines.extend([f"  --suite {suite} \\", f"  --run-id {run_id}"])
        return lines
    if kind == "reranking":
        lines = [
            "./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \\",
            f"  --strategy {summary.get('strategy', '<strategy>')} \\",
        ]
        if summary.get("model"):
            lines.append(f"  --model {summary['model']} \\")
        if summary.get("strategy") == "qwen3_causal_lm" and summary.get("qwen3_device"):
            lines.append(f"  --qwen3-device {summary['qwen3_device']} \\")
        if summary.get("strategy") == "qwen3_causal_lm" and summary.get("qwen3_max_length"):
            lines.append(f"  --qwen3-max-length {summary['qwen3_max_length']} \\")
        lines.extend([f"  --suite {suite} \\", f"  --run-id {run_id}"])
        return lines
    lines = [
        "./.venv/bin/python scripts/run_mem0_memory_benchmark.py \\",
        f"  --tool {summary.get('tool', 'cmd')} \\",
        f"  --suite {suite} \\",
    ]
    if summary.get("rerank_strategy"):
        lines.extend(
            [
                f"  --rerank-strategy {summary['rerank_strategy']} \\",
                f"  --recency-weight {summary.get('rerank_recency_weight', 0.2)} \\",
            ]
        )
    lines.append(f"  --run-id {run_id}")
    return lines


def decision_for(kind: str, summary: dict[str, Any]) -> tuple[str, str]:
    if kind == "memory+rerank" and summary.get("rerank_pass_rate") == 1.0:
        return (
            "keep testing",
            "Inline reranking fixed this seed recency suite, but raw vector ranking still failed and the suite is too small for default promotion.",
        )
    if kind == "memory":
        return (
            "keep testing",
            "The current mem0 path is functional and rollback-safe, but this run did not reach the strict 1.000 pass gate.",
        )
    if kind == "embedding":
        return (
            "keep testing",
            "The endpoint path is proven, but the embedding model still needs a recency or reranking fix before promotion beyond the current default.",
        )
    if kind == "extraction":
        if (
            summary.get("pass_rate") == 1.0
            and summary.get("json_validity_rate") == 1.0
            and summary.get("forbidden_hit_rate") == 0.0
            and summary.get("empty_case_pass_rate") == 1.0
        ):
            return (
                "keep testing",
                "The extractor passed the strict JSON, durable extraction, forbidden-hit, and empty-case gates; keep it as the rollback extractor until a larger replacement suite or stronger model beats it.",
            )
        return (
            "keep testing",
            "The extractor did not reach the JSON validity, durable extraction, and transient-noise gates needed for default promotion.",
        )
    if kind == "reranking":
        if summary.get("top1_accuracy") == 1.0:
            return (
                "keep testing",
                "The fixed suite passed, but learned and heuristic rerankers need a larger suite before live default integration.",
            )
        return (
            "keep testing",
            "This reranker did not reach the strict fixed-suite gate and should remain a comparison baseline.",
        )
    return (
        "keep testing",
        "Compare against the current default and relevant recency, distractor, latency, and rollback gates before promotion.",
    )


def render_card(kind: str, summary: dict[str, Any], summary_path: Path) -> str:
    model = summary.get("model") or summary.get("tool") or ""
    role = {
        "embedding": "embedder",
        "extraction": "extractor",
        "memory": "memory",
        "memory+rerank": "memory+rerank",
        "reranking": "reranker",
    }.get(kind, kind)
    endpoint = summary.get("base_url", "")
    runtime = summary.get("endpoint_kind") or summary.get("tool") or summary.get("strategy") or ("openai-compatible" if endpoint else "")
    output_dir = summary.get("output_dir", "")
    command = "\n".join(command_for_kind(kind, summary))
    decision, reason = decision_for(kind, summary)

    lines = [
        "# mem0 Run Card",
        "",
        f"Date: {summary.get('created_at', '')}",
        f"Run ID: {summary.get('run_id', '')}",
        f"Summary: `{summary_path}`",
        "",
        "## Candidate",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Role | {role} |",
        f"| Model/tool | `{model}` |" if model else "| Model/tool | |",
        f"| Runtime | {runtime} |",
        f"| Endpoint | `{endpoint}` |" if endpoint else "| Endpoint | |",
        "| Collection or index | |",
        f"| Embedding dims | {metric(summary, 'embedding_dims')} |",
        "| Distance metric | cosine / configured vector-store metric |",
        f"| Output | `{output_dir}` |" if output_dir else "| Output | |",
        "",
        "## Command",
        "",
        "```bash",
        "source scripts/env.sh",
        command,
        "```",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Pass rate / top-1 accuracy | {metric(summary, 'pass_rate', 'top1_accuracy')} |",
        f"| Rerank pass rate | {metric(summary, 'rerank_pass_rate')} |",
        f"| Recall@k / Recall@3 | {metric(summary, 'recall_at_k', 'recall_at_3')} |",
        f"| Top-1 expected rate | {metric(summary, 'top1_expected_rate', 'top1_accuracy')} |",
        f"| Recency conflict pass rate | {metric(summary, 'recency_conflict_pass_rate', 'rerank_recency_conflict_pass_rate')} |",
        f"| Distractor resistance pass rate | {metric(summary, 'distractor_resistance_pass_rate', 'rerank_distractor_resistance_pass_rate')} |",
        f"| JSON validity rate | {metric(summary, 'json_validity_rate')} |",
        f"| Add latency p50 | {metric(summary, 'add_latency_p50_s')} |",
        f"| Search/embed/extract latency p50 | {metric(summary, 'search_latency_p50_s', 'embed_latency_p50_s', 'latency_p50_s')} |",
        f"| Search/embed/extract latency p95 | {metric(summary, 'search_latency_p95_s', 'embed_latency_p95_s', 'latency_p95_s')} |",
        f"| Rerank latency p50 | {metric(summary, 'rerank_latency_p50_s')} |",
        "",
        "## Decision",
        "",
        f"Promote / keep testing / reject: {decision}",
        "",
        f"Reason: {reason}",
        "",
        "Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary = load_json(args.summary)
    kind = infer_kind(args.summary, summary)
    markdown = render_card(kind, summary, args.summary)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
