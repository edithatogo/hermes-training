#!/usr/bin/env python3
"""Build a constrained-envelope repair plan from completed local pilot results."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT / "reports/benchmark/coverage/prompt-profile-repair-results-20260614.json"
DEFAULT_JSON = ROOT / "reports/benchmark/coverage/constrained-envelope-repair-plan-20260614.json"
DEFAULT_MD = ROOT / "reports/benchmark/coverage/constrained-envelope-repair-plan-20260614.md"
STRICT_SUFFIX = (
    "Return exactly one Hermes tool-call JSON object or JSON array and no prose, "
    "no markdown, no analysis, no hidden reasoning, and no tags."
)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_number}: expected JSON object")
        rows.append(row)
    return rows


def source_files(source_summary: str) -> dict[str, str]:
    summary = Path(source_summary)
    return {
        "summary": str(summary),
        "results": str(summary.with_name("results.jsonl")),
        "responses": str(summary.with_name("responses.jsonl")),
    }


def classify_row(row: dict[str, Any]) -> str:
    reason = str(row.get("reason", ""))
    tool_calls = row.get("tool_calls")
    parse_errors = row.get("parse_errors")
    no_extra_text_ok = row.get("no_extra_text_ok")
    passed = bool(row.get("pass"))
    category = str(row.get("category", ""))

    if passed:
        if category and "invalid" in category:
            return "passed_refusal_case"
        return "passed_strict"
    if (
        "tool calls matched but extra text was present" in reason
        or (tool_calls and not parse_errors and no_extra_text_ok is False)
    ):
        return "matched_tool_calls_extra_text"
    if "excludes_ok=False" in reason or (category and "invalid" in category):
        return "refusal_boundary_failed"
    if row.get("response") == "":
        return "empty_output"
    if parse_errors or tool_calls == [] or "tool calls did not exactly match" in reason:
        return "malformed_or_no_calls"
    return "other_failure"


def priority_for(metrics: dict[str, int], best_pass_rate: float) -> str:
    if metrics["matched_tool_calls_extra_text"] > 0:
        return "high"
    if best_pass_rate > 0:
        return "medium"
    if metrics["passed_refusal_case"] > 0 and metrics["malformed_or_no_calls"] <= 1:
        return "medium"
    return "low"


def recommended_next_action(metrics: dict[str, int], priority: str) -> str:
    if priority == "high":
        return (
            "Implement a non-promotional constrained-envelope diagnostic that strips or suppresses "
            "reasoning only when the raw response already contains exact Hermes calls, then rerun "
            "strict no-extra-text scoring before any promotion claim."
        )
    if priority == "medium":
        return (
            "Defer promotion and try a targeted prompt/runtime variant only after the high-priority "
            "envelope diagnostic is proven."
        )
    return "Do not spend more local prompt-only cycles until runtime support or endpoint evidence changes."


def slug_for(candidate: str) -> str:
    return (
        candidate.lower()
        .replace("/", "-")
        .replace(".", "-")
        .replace("_", "-")
        .replace(" ", "-")
    )


def diagnostic_command(candidate: str, runner: str) -> str:
    slug = slug_for(candidate)
    common = (
        "source scripts/env.sh\n"
        "RUN_STAMP=$(date +%Y%m%d-%H%M%S)\n"
    )
    if runner == "endpoint":
        return (
            common +
            "./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py "
            "--suite benchmarks/endpoint_pilots/bfcl_pilot.json "
            f"--model '{candidate}' "
            "--base-url 'http://127.0.0.1:<port>/v1' "
            "--max-tokens 512 "
            "--require-no-extra-tool-text "
            f'--run-id "{slug}-constrained-envelope-diagnostic-${{RUN_STAMP}}" '
            f"--system-suffix '{STRICT_SUFFIX}'"
        )
    return (
        common +
        "./.venv/bin/python scripts/run_local_pilot_benchmark.py "
        "--suite benchmarks/endpoint_pilots/bfcl_pilot.json "
        f"--model '{candidate}' "
        "--max-tokens 512 "
        "--require-no-extra-tool-text "
        f'--run-id "{slug}-constrained-envelope-diagnostic-${{RUN_STAMP}}" '
        f"--system-suffix '{STRICT_SUFFIX}'"
    )


def build_plan(results_path: Path = DEFAULT_RESULTS, created_at: str | None = None) -> dict[str, Any]:
    results_data = load_json(results_path)
    result_rows = results_data.get("results", [])
    if not isinstance(result_rows, list) or not result_rows:
        raise ValueError(f"{results_path}: expected non-empty results list")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in result_rows:
        if not isinstance(row, dict):
            raise ValueError(f"{results_path}: result entries must be objects")
        grouped[str(row.get("candidate", "<unknown>"))].append(row)

    candidates: list[dict[str, Any]] = []
    for candidate, rows in grouped.items():
        metrics: dict[str, int] = defaultdict(int)
        variants: list[dict[str, Any]] = []
        source_missing: list[str] = []
        best_pass_rate = 0.0
        best_variant = ""
        best_runner = "local"

        for row in rows:
            source = source_files(str(row.get("source_summary", "")))
            results_file = Path(source["results"])
            case_counts: dict[str, int] = defaultdict(int)
            if results_file.exists():
                for case in load_jsonl(results_file):
                    classification = classify_row(case)
                    case_counts[classification] += 1
                    metrics[classification] += 1
            else:
                source_missing.append(str(results_file))
                metrics["missing_source_results"] += 1

            pass_rate = float(row.get("pass_rate", 0.0))
            if pass_rate >= best_pass_rate:
                best_pass_rate = pass_rate
                best_variant = str(row.get("variant", ""))
                best_runner = str(row.get("runner", "local"))
            variants.append(
                {
                    "variant": row.get("variant"),
                    "runner": row.get("runner"),
                    "status": row.get("status"),
                    "pass_rate": pass_rate,
                    "passed": row.get("passed"),
                    "cases": row.get("cases"),
                    "result_report": row.get("result_report"),
                    "source": source,
                    "case_classification_counts": dict(sorted(case_counts.items())),
                }
            )

        priority = priority_for(metrics, best_pass_rate)
        candidates.append(
            {
                "candidate": candidate,
                "priority": priority,
                "best_variant": best_variant,
                "best_runner": best_runner,
                "best_pass_rate": best_pass_rate,
                "case_metrics": dict(sorted(metrics.items())),
                "source_missing": source_missing,
                "recommended_next_action": recommended_next_action(metrics, priority),
                "promotion_boundary": (
                    "No promotion from this plan. Promotion requires raw strict or explicitly "
                    "documented runtime-wrapper gates with held-out BFCL, endpoint/local pilot, "
                    "official benchmark, latency, rollback, and publication evidence."
                ),
                "diagnostic_command": diagnostic_command(candidate, best_runner),
                "variants": variants,
            }
        )

    priority_order = {"high": 0, "medium": 1, "low": 2}
    candidates.sort(
        key=lambda item: (
            priority_order[item["priority"]],
            -int(item["case_metrics"].get("matched_tool_calls_extra_text", 0)),
            -float(item["best_pass_rate"]),
            item["candidate"],
        )
    )
    return {
        "run_id": "constrained-envelope-repair-plan-20260614",
        "created_at": created_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "source_results": str(results_path.relative_to(ROOT) if results_path.is_relative_to(ROOT) else results_path),
        "purpose": (
            "Rank completed prompt/profile repair failures for the next constrained-envelope "
            "or runtime-wrapper diagnostic without treating normalized or score-only behavior as promotion evidence."
        ),
        "promotion_allowed": False,
        "candidates": candidates,
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Constrained Envelope Repair Plan",
        "",
        f"Run ID: `{plan['run_id']}`",
        f"Created: `{plan['created_at']}`",
        "",
        plan["purpose"],
        "",
        "## Promotion Boundary",
        "",
        "This report is non-promotional. It may justify a constrained-envelope diagnostic, but it cannot promote a model.",
        "",
        "## Ranked Candidates",
        "",
        "| Candidate | Priority | Best variant | Best pass rate | Exact calls with extra text | Malformed/no calls | Action |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for candidate in plan["candidates"]:
        metrics = candidate["case_metrics"]
        lines.append(
            "| `{candidate}` | `{priority}` | `{variant}` | {pass_rate:.3f} | {extra} | {malformed} | {action} |".format(
                candidate=candidate["candidate"],
                priority=candidate["priority"],
                variant=candidate["best_variant"],
                pass_rate=float(candidate["best_pass_rate"]),
                extra=int(metrics.get("matched_tool_calls_extra_text", 0)),
                malformed=int(metrics.get("malformed_or_no_calls", 0)),
                action=candidate["recommended_next_action"],
            )
        )

    lines.extend(["", "## Diagnostic Commands", ""])
    for candidate in plan["candidates"]:
        lines.extend(
            [
                f"### {candidate['candidate']}",
                "",
                "Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.",
                "",
                "```bash",
                candidate["diagnostic_command"],
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-json", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--created-at")
    args = parser.parse_args()

    plan = build_plan(args.results_json, created_at=args.created_at)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    args.output_md.write_text(render_markdown(plan), encoding="utf-8")
    print(f"wrote {args.output_json}")
    print(f"wrote {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
