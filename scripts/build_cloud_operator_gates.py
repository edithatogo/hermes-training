#!/usr/bin/env python3
"""Build external operator gates for cloud scorecard backends."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_CHECKLIST = Path("reports/cloud/backend-unblock-checklist-20260613.json")
DEFAULT_JSON = Path("reports/cloud/cloud-operator-gates-20260614.json")
DEFAULT_MARKDOWN = Path("reports/cloud/cloud-operator-gates-20260614.md")


GATE_REQUIREMENTS: dict[str, list[str]] = {
    "colab": [
        "Colab keepalive/serviceusage permission fixed for project 1014160490159",
        "No active session conflict or intentionally owned session",
        "Recovered no-limit lm-eval artifacts",
    ],
    "hf_jobs": [
        "HF prepaid credits or grant capacity visible",
        "Explicit paid-compute approval for selected hardware",
        "Job ID/log URL and recovered Hub result artifacts",
    ],
    "azure": [
        "Azure login to the intended student account",
        "Azure for Students subscription selected",
        "GPU quota/workspace/compute/environment preflight passed",
        "Cost approval or zero-cost grant evidence",
    ],
    "ngc": [
        "NGC auth or SSO configured without committed secrets",
        "Org/team and Cloud Function GPU quota evidence",
        "Benchmark container image available in an accessible registry",
    ],
    "kaggle": [
        "Kernel completed",
        "Artifacts recovered to /Volumes/PortableSSD",
        "No-pending result ingest validation passed before any claim",
    ],
    "modal": [
        "Free credit, academic grant, or explicit paid-compute approval recorded in reports/cloud/modal-policy-evidence-20260614.json",
        "Modal policy gate reports execution_allowed=true",
        "Explicit Modal run approval",
        "Post-run Modal result ingest validation",
    ],
    "lightning": [
        "Lightning login and Teamspace owner configured",
        "Free credit/grant or explicit paid-compute approval",
        "Selected machine policy and artifact recovery path proven",
    ],
}


def load_checklist(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise ValueError(f"{path} does not look like a cloud unblock checklist")
    return data


def gate_rows(checklist: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in checklist["items"]:
        backend = str(item.get("backend", ""))
        rows.append(
            {
                "backend": backend,
                "status": item.get("status", "unknown"),
                "blocker": item.get("blocker", ""),
                "external_evidence_required": GATE_REQUIREMENTS.get(backend, ["Backend-specific operator evidence required"]),
                "safe_commands": item.get("commands", []),
                "execution_allowed": False,
                "promotion_allowed": False,
                "secret_policy": "Do not commit tokens, secrets, payment card details, private account IDs, or screenshots containing secrets.",
            }
        )
    return rows


def build_report(checklist_path: Path) -> dict[str, Any]:
    checklist = load_checklist(checklist_path)
    rows = gate_rows(checklist)
    return {
        "source_checklist": str(checklist_path),
        "status": "blocked-pending-operator-evidence",
        "execution_allowed": False,
        "promotion_allowed": False,
        "rows": rows,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Cloud Operator Gates",
        "",
        f"Source checklist: `{report['source_checklist']}`",
        "",
        "This report is fail-closed. It records external evidence needed before cloud execution or promotion.",
        "",
    ]
    for row in report["rows"]:
        lines.extend(
            [
                f"## {row['backend']}",
                "",
                f"- Status: `{row['status']}`",
                f"- Execution allowed: `{row['execution_allowed']}`",
                f"- Promotion allowed: `{row['promotion_allowed']}`",
                f"- Blocker: {row['blocker']}",
                "- External evidence required:",
            ]
        )
        for item in row["external_evidence_required"]:
            lines.append(f"  - {item}")
        lines.extend(["- Safe commands:", ""])
        lines.append("```bash")
        lines.extend(str(command) for command in row["safe_commands"])
        lines.append("```")
        lines.extend(["", f"- Secret policy: {row['secret_policy']}", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    report = build_report(args.checklist)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
