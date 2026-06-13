#!/usr/bin/env python3
"""Generate the current cloud backend unblock checklist from preflight state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_PREFLIGHT = Path("reports/cloud/backend-preflight-20260613.json")
DEFAULT_MARKDOWN = Path("reports/cloud/backend-unblock-checklist-20260613.md")
DEFAULT_JSON = Path("reports/cloud/backend-unblock-checklist-20260613.json")


def load_preflight(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("backends"), dict):
        raise ValueError(f"{path} does not look like a cloud backend preflight report")
    return data


def checklist_items(preflight: dict[str, Any]) -> list[dict[str, Any]]:
    backends = preflight["backends"]
    return [
        {
            "backend": "colab",
            "status": backends.get("colab", {}).get("status", "unknown"),
            "blocker": (
                "No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits "
                "HTTP 403 for project 1014160490159."
            ),
            "operator_actions": [
                "Confirm `colab sessions` is empty or intentionally owned.",
                "Fix Google Cloud service usage permission (`serviceusage.services.use`) for project 1014160490159 before another no-limit shard retry.",
                "If that permission cannot be fixed, prefer a persistent backend instead of repeated Colab retries.",
            ],
            "commands": [
                "PATH=\"$HOME/.local/bin:$PATH\" colab sessions",
                "./.venv/bin/python scripts/cloud_backend_preflight.py",
                "# after permission is fixed:",
                "./.venv/bin/python scripts/colab_lm_eval_shard.py launch --config reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-config-20260613.json --session qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry3 --gpu T4",
            ],
        },
        {
            "backend": "hf_jobs",
            "status": backends.get("hf_jobs", {}).get("status", "unknown"),
            "blocker": "HF Jobs rejected the live route probe with insufficient prepaid credits.",
            "operator_actions": [
                "Add Hugging Face prepaid credits or grant capacity.",
                "Keep paid GPU submission explicitly confirmation-gated.",
                "Submit the prepared scorecard only after credits are visible.",
            ],
            "commands": [
                "hf jobs ps",
                "./.venv/bin/python scripts/submit_hf_jobs_peft_scorecard.py",
                "./.venv/bin/python scripts/submit_hf_jobs_peft_scorecard.py --execute --confirm-paid-compute",
            ],
        },
        {
            "backend": "azure",
            "status": backends.get("azure", {}).get("status", "unknown"),
            "blocker": "Azure CLI is installed but not currently logged in.",
            "operator_actions": [
                "Run device-code login for the intended account.",
                "Select `Azure for Students` if available.",
                "Rerun quota checks before any workspace, compute, or job action.",
            ],
            "commands": [
                "az login --use-device-code",
                "az account set --subscription \"Azure for Students\"",
                "./.venv/bin/python scripts/azure_preflight.py --check-quota --region australiaeast",
                "./.venv/bin/python scripts/azure_status.py",
                "./.venv/bin/python scripts/submit_azure_peft_scorecard.py",
                "./.venv/bin/python scripts/submit_azure_peft_scorecard.py --execute --confirm-azure-run",
            ],
        },
        {
            "backend": "ngc",
            "status": backends.get("ngc", {}).get("status", "unknown"),
            "blocker": "NGC has no configured API key, SSO session, org/team, GPU quota, or benchmark container.",
            "operator_actions": [
                "Authenticate with SSO or supplied API key without committing secrets.",
                "Record non-secret org/team and Cloud Function GPU quota evidence.",
                "Build or select an NGC registry benchmark container before any task submission.",
            ],
            "commands": [
                "ngc sso login",
                "ngc config current",
                "ngc cloud-function gpu quota",
                "ngc cloud-function task create --help",
                "./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py",
                "./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py --container-image <ngc-registry-image> --gpu-specification <gpu-spec> --execute --confirm-ngc-run",
            ],
        },
        {
            "backend": "kaggle",
            "status": backends.get("kaggle", {}).get("status", "unknown"),
            "blocker": "Kaggle CLI is installed but unauthenticated.",
            "operator_actions": [
                "Authenticate Kaggle CLI with OAuth or an API token.",
                "Check weekly accelerator quota before pushing a kernel.",
                "Push the staged kernel only after explicit confirmation.",
            ],
            "commands": [
                "kaggle auth login",
                "kaggle quota",
                "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py",
                "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py --execute --confirm-kaggle-run",
            ],
        },
    ]


def render_markdown(items: list[dict[str, Any]], source: Path) -> str:
    lines = [
        "# Cloud Backend Unblock Checklist",
        "",
        f"Source preflight: `{source}`",
        "",
        "This checklist is fail-closed. It records the next operator actions but does not run login, paid compute, or remote jobs.",
        "",
    ]
    for item in items:
        lines.extend(
            [
                f"## {item['backend']}",
                "",
                f"- Status: `{item['status']}`",
                f"- Blocker: {item['blocker']}",
                "- Operator actions:",
            ]
        )
        for action in item["operator_actions"]:
            lines.append(f"  - {action}")
        lines.extend(["- Commands:", ""])
        lines.append("```bash")
        lines.extend(item["commands"])
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", type=Path, default=DEFAULT_PREFLIGHT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    args = parser.parse_args()

    preflight = load_preflight(args.preflight)
    items = checklist_items(preflight)
    payload = {"source_preflight": str(args.preflight), "items": items}

    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text(render_markdown(items, args.preflight), encoding="utf-8")
    args.json_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
