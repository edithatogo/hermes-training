#!/usr/bin/env python3
"""Summarize mem0 benchmark summary.json files into one markdown table."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_summary(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def format_float(value: Any) -> str:
    if isinstance(value, int | float):
        return f"{float(value):.3f}"
    return ""


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
    return "unknown"


def render_markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# mem0 Benchmark Index",
        "",
        "| Kind | Run ID | Model/Tool | Raw Pass | Rerank Pass | Top-1 | Recall@k/3 | JSON Valid | Latency p50 | Output |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        summary = row["summary"]
        kind = row["kind"]
        model_or_tool = summary.get("model") or summary.get("tool") or ""
        if kind == "reranking" and not model_or_tool:
            model_or_tool = summary.get("strategy") or ""
        raw_pass = summary.get("pass_rate", summary.get("top1_accuracy"))
        rerank_pass = summary.get("rerank_pass_rate")
        top1 = summary.get("top1_expected_rate", summary.get("top1_accuracy"))
        recall = summary.get("recall_at_k", summary.get("recall_at_3"))
        json_valid = summary.get("json_validity_rate")
        latency = summary.get("search_latency_p50_s", summary.get("latency_p50_s", summary.get("embed_latency_p50_s", summary.get("rerank_latency_p50_s"))))
        output = summary.get("output_dir", "")
        lines.append(
            "| "
            + " | ".join(
                [
                    kind,
                    str(summary.get("run_id", "")),
                    str(model_or_tool),
                    format_float(raw_pass),
                    format_float(rerank_pass),
                    format_float(top1),
                    format_float(recall),
                    format_float(json_valid),
                    format_float(latency),
                    f"`{output}`" if output else "",
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    for path in args.paths:
        summary = load_summary(path)
        rows.append({"path": path, "kind": infer_kind(path, summary), "summary": summary})
    rows.sort(key=lambda row: (row["kind"], str(row["summary"].get("run_id", ""))))
    markdown = render_markdown(rows)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
