#!/usr/bin/env python3
"""Build a machine-readable standard benchmark coverage report."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATE = "qwen3-4b-strict-toolcall-v4-targeted"
DEFAULT_RUN_ID = "qwen3-v4-targeted-standard-coverage-20260526"
DEFAULT_OUTPUT_ROOT = ROOT / "reports" / "benchmark" / "standard-coverage"


@dataclass(frozen=True)
class CoverageItem:
    suite: str
    tier: str
    status: str
    evidence: str
    metric: str
    notes: str
    required_for: str

    def to_dict(self) -> dict[str, str]:
        return {
            "suite": self.suite,
            "tier": self.tier,
            "status": self.status,
            "evidence": self.evidence,
            "metric": self.metric,
            "notes": self.notes,
            "required_for": self.required_for,
        }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_first(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_table_value(label: str, text: str) -> str:
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] == label:
            for cell in reversed(cells[1:]):
                if re.fullmatch(r"[0-9.]+", cell):
                    return cell
    return ""


def exists_status(path: Path, suite: str, tier: str, metric: str, notes: str, required_for: str) -> CoverageItem:
    status = "present" if path.exists() else "missing"
    return CoverageItem(suite, tier, status, str(path.relative_to(ROOT)), metric if path.exists() else "", notes, required_for)


def build_items(candidate: str) -> list[CoverageItem]:
    if candidate != DEFAULT_CANDIDATE:
        raise ValueError(f"Unsupported candidate for the built-in coverage map: {candidate}")

    publication_gate = ROOT / "reports" / "benchmark" / "publication-readiness-gate-20260524.md"
    pilots = ROOT / "reports" / "benchmark" / "local-pilots" / "qwen3-4b-strict-toolcall-v4-targeted-local-pilots-20260525.md"
    official_ifeval = ROOT / "reports" / "benchmark" / "official-ifeval" / "qwen3-4b-v4-targeted-ifeval-pilot-20260526.md"
    lm_eval_selected = ROOT / "reports" / "benchmark" / "lm-eval" / "qwen3-4b-v4-targeted-lm-eval-selected-smoke-20260526.md"
    bundle = ROOT / "reports" / "publication" / "qwen3-4b-strict-toolcall-v4-targeted"
    readiness = bundle / "publish-readiness-checklist.md"

    gate_text = read_text(publication_gate)
    pilots_text = read_text(pilots)
    ifeval_text = read_text(official_ifeval)
    readiness_text = read_text(readiness)

    items = [
        CoverageItem(
            suite="local-heldout-strict-tool-call",
            tier="candidate-local",
            status="passed" if "`1.000`" in gate_text and publication_gate.exists() else "missing",
            evidence=str(publication_gate.relative_to(ROOT)),
            metric="strict held-out pass 1.000" if publication_gate.exists() else "",
            notes="Required Hermes-agent publication gate under the recorded Qwen runtime prefill condition.",
            required_for="local adapter publication claim",
        ),
        CoverageItem(
            suite="local-bfcl-style-pilot",
            tier="pilot",
            status="present" if pilots.exists() else "missing",
            evidence=str(pilots.relative_to(ROOT)),
            metric=f"BFCL-style pilot {extract_table_value('BFCL-style pilot', pilots_text)}",
            notes="Repo-native pilot only; not an official BFCL score.",
            required_for="pilot-only model card positioning",
        ),
        CoverageItem(
            suite="local-ifeval-style-pilot",
            tier="pilot",
            status="present" if pilots.exists() else "missing",
            evidence=str(pilots.relative_to(ROOT)),
            metric=f"IFEval-style pilot {extract_table_value('IFEval-style pilot', pilots_text)}",
            notes="Repo-native prompt subset only; official IFEval is tracked separately.",
            required_for="pilot-only model card positioning",
        ),
        CoverageItem(
            suite="local-coding-sanity-pilot",
            tier="pilot",
            status="present" if pilots.exists() else "missing",
            evidence=str(pilots.relative_to(ROOT)),
            metric=f"coding sanity pilot {extract_table_value('Coding sanity pilot', pilots_text)}",
            notes="Small local coding sanity set; not HumanEval, MBPP, BigCodeBench, or LiveCodeBench.",
            required_for="pilot-only model card positioning",
        ),
        CoverageItem(
            suite="official-ifeval-pilot",
            tier="official-pilot",
            status="present" if official_ifeval.exists() else "missing",
            evidence=str(official_ifeval.relative_to(ROOT)),
            metric=f"prompt strict {extract_table_value('Prompt-level strict accuracy', ifeval_text)}",
            notes="Official harness path is proven with a 25-sample limit; not a leaderboard score.",
            required_for="official harness readiness",
        ),
        CoverageItem(
            suite="publication-bundle",
            tier="release-gate",
            status="blocked" if "Human publication approval recorded." in readiness_text else "missing",
            evidence=str(readiness.relative_to(ROOT)),
            metric="local quality gates checked; public release gates remain blocked",
            notes="Dataset/model publication still needs explicit approval and final public-release gates.",
            required_for="public Hugging Face release",
        ),
        CoverageItem(
            suite="official-bfcl",
            tier="official-candidate",
            status="missing",
            evidence="",
            metric="",
            notes="Official BFCL remains future work; local BFCL-style pilot is not a substitute.",
            required_for="broad tool-calling benchmark claim",
        ),
        CoverageItem(
            suite="lm-eval-selected",
            tier="official-candidate",
            status="blocked" if lm_eval_selected.exists() else "missing",
            evidence=str(lm_eval_selected.relative_to(ROOT)) if lm_eval_selected.exists() else "",
            metric="",
            notes="Selected lm-eval smoke was attempted; current mlx_lm.server endpoint is not loglikelihood-compatible for these tasks.",
            required_for="general benchmark claim",
        ),
        CoverageItem(
            suite="official-coding",
            tier="official-candidate",
            status="missing",
            evidence="",
            metric="",
            notes="No HumanEval/MBPP/EvalPlus/BigCodeBench/LiveCodeBench scorecard is recorded.",
            required_for="coding benchmark claim",
        ),
        CoverageItem(
            suite="safety-refusal",
            tier="official-candidate",
            status="missing",
            evidence="",
            metric="",
            notes="No XSTest/SimpleSafetyTests/HarmBench subset scorecard is recorded.",
            required_for="safety/refusal claim",
        ),
        CoverageItem(
            suite="ruler-long-context",
            tier="official-candidate",
            status="missing",
            evidence="",
            metric="",
            notes="No RULER staged-context scorecard is recorded.",
            required_for="long-context claim",
        ),
    ]
    return items


def summarize(items: list[CoverageItem], candidate: str, run_id: str) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item.status] = counts.get(item.status, 0) + 1
    local_ready = any(item.suite == "local-heldout-strict-tool-call" and item.status == "passed" for item in items)
    official_missing = [item.suite for item in items if item.tier == "official-candidate" and item.status == "missing"]
    public_blocked = any(item.suite == "publication-bundle" and item.status == "blocked" for item in items)
    return {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "candidate": candidate,
        "status": "pilot-only" if local_ready and official_missing else "incomplete",
        "local_adapter_gate_ready": local_ready,
        "public_release_blocked": public_blocked,
        "official_candidate_missing": official_missing,
        "counts": counts,
        "items": [item.to_dict() for item in items],
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# Standard Benchmark Coverage: {summary['candidate']}",
        "",
        f"Run ID: `{summary['run_id']}`",
        f"Status: `{summary['status']}`",
        f"Local adapter gate ready: `{str(summary['local_adapter_gate_ready']).lower()}`",
        f"Public release blocked: `{str(summary['public_release_blocked']).lower()}`",
        "",
        "## Coverage",
        "",
        "| Suite | Tier | Status | Metric | Evidence | Required for |",
        "|---|---|---|---|---|---|",
    ]
    for item in summary["items"]:
        evidence = item["evidence"] or "none"
        lines.append(
            f"| `{item['suite']}` | {item['tier']} | `{item['status']}` | {item['metric']} | {evidence} | {item['required_for']} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "The adapter can be described as local strict Hermes-agent evidence with pilot-only benchmark support.",
            "Do not describe it as broadly benchmarked until the missing official candidate suites are run or explicitly excluded.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", default=DEFAULT_CANDIDATE)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--md-output", type=Path)
    parser.add_argument("--require-official-candidate", action="store_true")
    parser.add_argument("--no-write", action="store_true", help="Print the generated summary without updating report files.")
    args = parser.parse_args()

    items = build_items(args.candidate)
    summary = summarize(items, args.candidate, args.run_id)
    if not args.no_write:
        args.output_root.mkdir(parents=True, exist_ok=True)
        json_output = args.json_output or args.output_root / f"{args.run_id}.json"
        md_output = args.md_output or args.output_root / f"{args.run_id}.md"
        json_output.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        md_output.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if args.require_official_candidate and summary["official_candidate_missing"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
