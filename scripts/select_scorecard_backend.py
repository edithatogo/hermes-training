#!/usr/bin/env python3
"""Build a fail-closed backend selection report for Qwen3 v4 PEFT scorecards."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHECKLIST = ROOT / "reports/cloud/backend-unblock-checklist-20260613.json"
DEFAULT_KAGGLE_INGEST = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-result-ingest-rerun-p100-v7-20260614.json"
DEFAULT_JSON = ROOT / "reports/cloud/qwen3-v4-peft-scorecard-backend-selection-20260614.json"
DEFAULT_MD = ROOT / "reports/cloud/qwen3-v4-peft-scorecard-backend-selection-20260614.md"

PRIORITY = {
    "prepared-needs-run-approval": 100,
    "prepared-needs-credit-and-gpu-policy-check": 70,
    "prepared-needs-quota-check": 65,
    "prepared-needs-paid-compute-approval": 60,
    "completed-validated-scorecard": 55,
    "ready": 40,
    "blocked-insufficient-hf-credits": 20,
}

REMOTE_EXECUTION_BLOCKERS = {
    "explicit run approval",
    "cost or zero-cost policy confirmation",
    "artifact recovery plan",
}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def backend_score(item: dict[str, Any], kaggle_ingest: dict[str, Any] | None = None) -> int:
    status = str(item.get("status", "unknown"))
    score = PRIORITY.get(status, 0)
    backend = str(item.get("backend", ""))
    blocker = str(item.get("blocker", "")).lower()
    if backend == "colab" and ("prune" in blocker or "keepalive" in blocker):
        score -= 35
    if backend == "kaggle" and kaggle_ingest:
        if kaggle_ingest.get("status") == "fail":
            score -= 80
        elif kaggle_ingest.get("status") == "pass":
            score += 45
    if backend in {"kaggle", "azure", "hf_jobs", "modal", "lightning", "ngc"}:
        score += 5
    return score


def kaggle_blocker_suffix(kaggle_ingest: dict[str, Any] | None) -> str:
    if not kaggle_ingest:
        return ""
    if kaggle_ingest.get("status") == "fail":
        return " Live Kaggle ingest failed after a completed kernel run; do not retry unchanged P100/CUDA path."
    if kaggle_ingest.get("status") == "pass":
        return " Kaggle v7 recovered a no-limit five-task scorecard and passed the no-pending ingest gate."
    return ""


def select_backends(checklist: dict[str, Any], kaggle_ingest: dict[str, Any] | None = None) -> dict[str, Any]:
    items = checklist.get("items", [])
    if not isinstance(items, list):
        raise ValueError("checklist items must be a list")
    candidates: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        blocker = str(item.get("blocker", ""))
        suffix = kaggle_blocker_suffix(kaggle_ingest) if item.get("backend") == "kaggle" else ""
        if item.get("status") == "completed-validated-scorecard":
            suffix = ""
        if suffix and suffix.strip() in blocker:
            suffix = ""
        row = {
            "backend": item.get("backend"),
            "status": item.get("status"),
            "score": backend_score(item, kaggle_ingest),
            "blocker": f"{blocker}{suffix}",
            "operator_actions": item.get("operator_actions", []),
            "commands": item.get("commands", []),
        }
        candidates.append(row)
    candidates.sort(key=lambda row: (-int(row["score"]), str(row["backend"])))
    selected = candidates[0] if candidates else None
    if selected and selected.get("status") == "completed-validated-scorecard":
        decision = (
            "Use the recovered Kaggle v7 artifacts as the selected no-limit scorecard evidence. "
            "Keep any future remote execution behind the listed operator gates."
        )
    else:
        decision = (
            "Use the selected backend only after the listed operator gates pass. "
            "Do not retry Colab no-limit shards while keepalive/session-pruning blockers remain."
            " Do not retry Kaggle unchanged after a failed live ingest."
        )
    return {
        "status": "blocked-pending-operator-gates",
        "execute": False,
        "promotion_allowed": False,
        "source_checklist": checklist.get("source_preflight", "reports/cloud/backend-preflight-20260613.json"),
        "selected_backend": selected["backend"] if selected else None,
        "selected_status": selected["status"] if selected else None,
        "selected_score": selected["score"] if selected else None,
        "required_before_execution": sorted(REMOTE_EXECUTION_BLOCKERS),
        "decision": decision,
        "ranked_backends": candidates,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 v4 PEFT Scorecard Backend Selection",
        "",
        f"- Status: `{payload['status']}`",
        f"- Execute: `{str(payload['execute']).lower()}`",
        f"- Promotion allowed: `{str(payload['promotion_allowed']).lower()}`",
        f"- Selected backend: `{payload['selected_backend']}`",
        f"- Selected backend status: `{payload['selected_status']}`",
        "",
        payload["decision"],
        "",
        "## Required Before Execution",
        "",
    ]
    for gate in payload["required_before_execution"]:
        lines.append(f"- {gate}")
    lines.extend(["", "## Ranked Backends", "", "| Rank | Backend | Status | Score | Blocker |", "|---:|---|---|---:|---|"])
    for index, row in enumerate(payload["ranked_backends"], start=1):
        blocker = str(row["blocker"]).replace("|", "\\|")
        lines.append(f"| {index} | `{row['backend']}` | `{row['status']}` | {row['score']} | {blocker} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    parser.add_argument("--kaggle-ingest", type=Path, default=DEFAULT_KAGGLE_INGEST)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    kaggle_ingest = load_json(args.kaggle_ingest) if args.kaggle_ingest.exists() else None
    payload = select_backends(load_json(args.checklist), kaggle_ingest)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(payload), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
