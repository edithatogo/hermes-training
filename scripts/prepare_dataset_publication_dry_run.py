#!/usr/bin/env python3
"""Prepare a non-publishing Hugging Face dataset release approval artifact."""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from audit_publication_dataset_sources import summarize as summarize_sources
except ModuleNotFoundError:
    from scripts.audit_publication_dataset_sources import summarize as summarize_sources


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_DIR = Path("/Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526")
DEFAULT_BUNDLE_DIR = ROOT / "reports" / "publication" / "qwen3-4b-strict-toolcall-v4-targeted"
DEFAULT_REPO_ID = "edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4"
DEFAULT_RUN_ID = "dataset-publication-dry-run-20260526"
REQUIRED_EVIDENCE = (
    "cleaned-synthetic-source-audit.json",
    "cleaned-synthetic-overlap-audit.json",
    "cleaned-synthetic-token-audit.json",
    "hf-dataset-card-draft.md",
    "dataset-publication-scope.md",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_dataset_manifest(dataset_dir: Path) -> dict[str, Any]:
    source_summary = summarize_sources(dataset_dir)
    files = sorted(path for path in dataset_dir.glob("*.jsonl"))
    return {
        "dataset_dir": str(dataset_dir),
        "files": [path.name for path in files],
        "rows": source_summary["rows"],
        "unique_ids": source_summary["unique_ids"],
        "duplicate_id_count": source_summary["duplicate_id_count"],
        "split_counts": source_summary["split_counts"],
        "source_counts": source_summary["source_counts"],
        "unknown_sources": source_summary["unknown_sources"],
        "review_result": source_summary["review_result"],
        "public_dataset_release": source_summary["public_dataset_release"],
    }


def load_publication_evidence(bundle_dir: Path) -> dict[str, Any]:
    evidence: dict[str, Any] = {
        "bundle_dir": str(bundle_dir),
        "required_files": {},
    }
    for name in REQUIRED_EVIDENCE:
        path = bundle_dir / name
        evidence["required_files"][name] = path.exists()
    for name in (
        "cleaned-synthetic-source-audit.json",
        "cleaned-synthetic-overlap-audit.json",
        "cleaned-synthetic-token-audit.json",
    ):
        path = bundle_dir / name
        evidence[name] = load_json(path) if path.exists() else {}
    scope_path = bundle_dir / "dataset-publication-scope.md"
    scope_text = scope_path.read_text(encoding="utf-8") if scope_path.exists() else ""
    evidence["scope_blocks_publication"] = "Public dataset publication remains blocked." in scope_text
    evidence["approval_required"] = "explicit human approval" in scope_text.lower()
    return evidence


def validate_dataset_release_blocked(dataset: dict[str, Any], evidence: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    missing = [name for name, exists in evidence["required_files"].items() if not exists]
    if missing:
        blockers.append(f"missing evidence files: {', '.join(missing)}")
    if dataset["unknown_sources"]:
        blockers.append(f"unknown dataset sources: {', '.join(dataset['unknown_sources'])}")
    if dataset["duplicate_id_count"]:
        blockers.append(f"duplicate IDs present: {dataset['duplicate_id_count']}")
    source_audit = evidence.get("cleaned-synthetic-source-audit.json", {})
    if source_audit.get("public_dataset_release") != "blocked_pending_human_scope_approval":
        blockers.append("source audit does not preserve the public dataset blocker")
    overlap = evidence.get("cleaned-synthetic-overlap-audit.json", {})
    if overlap.get("error_count") not in (0, None):
        blockers.append(f"overlap audit has errors: {overlap.get('error_count')}")
    if not evidence.get("scope_blocks_publication"):
        blockers.append("dataset publication scope document does not state the public-release blocker")
    if not evidence.get("approval_required"):
        blockers.append("dataset publication scope document does not require explicit human approval")
    blockers.append("explicit human approval for the cleaned synthetic-only dataset scope is still required")
    return blockers


def build_plan(dataset_dir: Path, bundle_dir: Path, repo_id: str, run_id: str) -> dict[str, Any]:
    dataset = collect_dataset_manifest(dataset_dir)
    evidence = load_publication_evidence(bundle_dir)
    blockers = validate_dataset_release_blocked(dataset, evidence)
    return {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "status": "dry-run-only",
        "publish_actions_performed": False,
        "intended_repo_id": repo_id,
        "dataset": dataset,
        "evidence": evidence,
        "blockers": blockers,
        "approval_phrase": (
            "I approve publishing the cleaned synthetic-only dataset at "
            f"{dataset_dir} to Hugging Face dataset repo {repo_id}."
        ),
    }


def render_approval_artifact(plan: dict[str, Any]) -> str:
    dataset = plan["dataset"]
    evidence = plan["evidence"]
    lines = [
        f"# Dataset Publication Dry Run: {plan['run_id']}",
        "",
        f"Created: `{plan['created_at']}`",
        f"Status: `{plan['status']}`",
        f"Publish actions performed: `{str(plan['publish_actions_performed']).lower()}`",
        f"Intended Hugging Face dataset repo: `{plan['intended_repo_id']}`",
        "",
        "## Dataset",
        "",
        f"- Path: `{dataset['dataset_dir']}`",
        f"- Files: `{', '.join(dataset['files'])}`",
        f"- Rows: `{dataset['rows']}`",
        f"- Unique IDs: `{dataset['unique_ids']}`",
        f"- Duplicate IDs: `{dataset['duplicate_id_count']}`",
        f"- Review result: `{dataset['review_result']}`",
        "",
        "## Splits",
        "",
        "| Split file | Rows |",
        "|---|---:|",
    ]
    for split, count in dataset["split_counts"].items():
        lines.append(f"| `{split}` | {count} |")
    lines.extend(["", "## Sources", "", "| Source | Rows |", "|---|---:|"])
    for source, count in dataset["source_counts"].items():
        lines.append(f"| `{source}` | {count} |")
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            "| File | Present |",
            "|---|---:|",
        ]
    )
    for name, present in evidence["required_files"].items():
        lines.append(f"| `{name}` | `{str(present).lower()}` |")
    overlap = evidence.get("cleaned-synthetic-overlap-audit.json", {})
    token = evidence.get("cleaned-synthetic-token-audit.json", {})
    lines.extend(
        [
            "",
            "## Audit Summary",
            "",
            f"- Overlap audit error count: `{overlap.get('error_count', 'unknown')}`",
            f"- Held-out prompt overlap count: `{overlap.get('overlap', {}).get('heldout_suite', {}).get('user_prompt_overlap_count', 'unknown')}`",
            f"- Token audit model: `{token.get('model', 'unknown')}`",
            "",
            "## Blockers",
            "",
        ]
    )
    for blocker in plan["blockers"]:
        lines.append(f"- {blocker}")
    lines.extend(
        [
            "",
            "## Required Approval",
            "",
            "To publish later, record this exact approval after reviewing the scope:",
            "",
            "```text",
            plan["approval_phrase"],
            "```",
            "",
            "This dry run did not call `hf repo create`, `hf upload`, or any other publishing command.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR)
    parser.add_argument("--bundle-dir", type=Path, default=DEFAULT_BUNDLE_DIR)
    parser.add_argument("--repo-id", default=DEFAULT_REPO_ID)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    plan = build_plan(args.dataset_dir, args.bundle_dir, args.repo_id, args.run_id)
    output = args.output or args.bundle_dir / f"{args.run_id}.md"
    json_output = args.json_output or args.bundle_dir / f"{args.run_id}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_approval_artifact(plan), encoding="utf-8")
    json_output.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "json_output": str(json_output), "status": plan["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
