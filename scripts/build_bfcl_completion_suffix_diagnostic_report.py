#!/usr/bin/env python3
"""Build the Qwen3 v4 BFCL completion-suffix diagnostic report."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLEAN_RUN_ROOT = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/"
    "qwen3-v4-peft-official-bfcl-clean-rerun-20260624"
)
SERIAL_RUN_ROOT = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/"
    "qwen3-v4-peft-official-bfcl-serial-20260624"
)
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-bfcl-completion-suffix-diagnostic-20260624.json"
DEFAULT_MD = DEFAULT_JSON.with_suffix(".md")
PROXY_SCRIPT = ROOT / "scripts/openai_normalizing_proxy.py"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
    return rows


def classify_result(value: Any) -> str:
    text = str(value or "")
    if text.strip() == "":
        return "blank"
    if "<tool_call>" in text or '"name"' in text:
        return "tool_like"
    return "other_nonblank"


def summarize_run(run_root: Path) -> dict[str, Any]:
    result_root = run_root / "results/Qwen_Qwen3-4B-Instruct-2507-FC/non_live"
    files = sorted(result_root.glob("BFCL_v4_*_result.json"))
    categories: dict[str, dict[str, Any]] = {}
    aggregate: Counter[str] = Counter()
    for path in files:
        category = path.name.removeprefix("BFCL_v4_").removesuffix("_result.json")
        rows = read_jsonl(path)
        counts = Counter(classify_result(row.get("result")) for row in rows)
        aggregate.update(counts)
        categories[category] = {
            "path": str(path),
            "rows": len(rows),
            "blank_rows": int(counts.get("blank", 0)),
            "tool_like_rows": int(counts.get("tool_like", 0)),
            "other_nonblank_rows": int(counts.get("other_nonblank", 0)),
            "sample_outputs": [str(row.get("result", "")).replace("\n", "\\n")[:160] for row in rows[:3]],
        }
    total_rows = sum(item["rows"] for item in categories.values())
    blank_rows = int(aggregate.get("blank", 0))
    return {
        "run_root": str(run_root),
        "result_files": len(files),
        "total_rows": total_rows,
        "blank_rows": blank_rows,
        "tool_like_rows": int(aggregate.get("tool_like", 0)),
        "other_nonblank_rows": int(aggregate.get("other_nonblank", 0)),
        "blank_rate": (blank_rows / total_rows) if total_rows else None,
        "categories": categories,
    }


def proxy_supports_completion_suffix(proxy_script: Path = PROXY_SCRIPT) -> bool:
    text = proxy_script.read_text(encoding="utf-8")
    return "--completion-prompt-suffix" in text and "add_completions_prompt_suffix" in text


def build_report(clean_run_root: Path = CLEAN_RUN_ROOT, serial_run_root: Path = SERIAL_RUN_ROOT) -> dict[str, Any]:
    clean = summarize_run(clean_run_root)
    serial = summarize_run(serial_run_root)
    proxy_support = proxy_supports_completion_suffix()
    gate_ready = (
        proxy_support
        and serial["total_rows"] > 0
        and serial["blank_rows"] > 0
        and serial["tool_like_rows"] == 0
    )
    return {
        "report_id": "qwen3-v4-bfcl-completion-suffix-diagnostic-20260624",
        "candidate": "qwen3-4b-strict-toolcall-v4-targeted",
        "suite": "official-bfcl-selected-slice",
        "status": "runtime-bridge-ready-for-bounded-rerun" if gate_ready else "diagnostic-incomplete",
        "proxy_supports_completion_prompt_suffix": proxy_support,
        "completion_prompt_suffix": "<tool_call>",
        "clean_rerun": clean,
        "serial_partial_without_suffix": serial,
        "decision": (
            "The clean endpoint/proxy path no longer shows upstream errors, but BFCL completions are whitespace-only "
            "when the completion prompt ends at the assistant marker. The next bounded rerun should route /v1/completions "
            "through the proxy with --completion-prompt-suffix '<tool_call>' and stop after a small gate if outputs remain blank."
        ),
        "gate": {
            "passed": False,
            "reason": "Runtime bridge is ready for a bounded rerun, but no completion-suffix BFCL score is recorded yet.",
            "next_rerun_gate": [
                "upstream_error_rows == 0",
                "blank_output_rows == 0 on the gated 10-case slice",
                "tool-like completion rows > 0 before expanding beyond the gated slice",
            ],
        },
        "publication_boundary": (
            "Diagnostic/runtime-bridge evidence only. This does not create a BFCL score claim and does not change model weights."
        ),
    }


def render_markdown(report: dict[str, Any]) -> str:
    clean = report["clean_rerun"]
    serial = report["serial_partial_without_suffix"]
    lines = [
        "# Qwen3 v4 BFCL Completion-Suffix Diagnostic",
        "",
        f"- Status: `{report['status']}`",
        f"- Proxy supports completion prompt suffix: `{str(report['proxy_supports_completion_prompt_suffix']).lower()}`",
        f"- Proposed suffix: `{report['completion_prompt_suffix']}`",
        "",
        "## Evidence",
        "",
        "| Run | Rows | Blank rows | Tool-like rows | Blank rate |",
        "|---|---:|---:|---:|---:|",
        (
            f"| Clean gated rerun | {clean['total_rows']} | {clean['blank_rows']} | "
            f"{clean['tool_like_rows']} | {clean['blank_rate']:.3f} |"
            if clean["blank_rate"] is not None
            else "| Clean gated rerun | 0 | 0 | 0 | N/A |"
        ),
        (
            f"| Serial partial without suffix | {serial['total_rows']} | {serial['blank_rows']} | "
            f"{serial['tool_like_rows']} | {serial['blank_rate']:.3f} |"
            if serial["blank_rate"] is not None
            else "| Serial partial without suffix | 0 | 0 | 0 | N/A |"
        ),
        "",
        "## Decision",
        "",
        report["decision"],
        "",
        "## Gate",
        "",
        f"- Passed: `{str(report['gate']['passed']).lower()}`",
        f"- Reason: {report['gate']['reason']}",
        "",
        "## Boundary",
        "",
        report["publication_boundary"],
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean-run-root", type=Path, default=CLEAN_RUN_ROOT)
    parser.add_argument("--serial-run-root", type=Path, default=SERIAL_RUN_ROOT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()
    report = build_report(args.clean_run_root, args.serial_run_root)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(f"wrote {args.json_output}")
    print(f"wrote {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
