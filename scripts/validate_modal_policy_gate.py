#!/usr/bin/env python3
"""Validate the Modal zero-cost policy gate before any GPU scorecard run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BILLING = ROOT / "reports/cloud/modal-billing-this-month-20260614.json"
DEFAULT_PREFLIGHT = ROOT / "reports/cloud/backend-preflight-20260613.json"
DEFAULT_DRY_RUN = ROOT / "reports/cloud/qwen3-v4-peft-modal-submit-dry-run-20260614.json"
DEFAULT_POLICY_EVIDENCE = ROOT / "reports/cloud/modal-policy-evidence-20260614.json"
DEFAULT_JSON = ROOT / "reports/cloud/modal-policy-gate-20260614.json"
DEFAULT_MARKDOWN = ROOT / "reports/cloud/modal-policy-gate-20260614.md"


def load_optional_json(path: Path) -> Any | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": passed, "detail": detail})


def modal_status(preflight: Any | None) -> str:
    if not isinstance(preflight, dict):
        return "missing-preflight"
    return str(preflight.get("backends", {}).get("modal", {}).get("status", "unknown"))


def validate_policy_evidence(evidence: Any | None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    checks: list[dict[str, Any]] = []
    if evidence is None:
        add_check(checks, "policy_evidence_present", True, "optional evidence file is absent; execution remains blocked")
        return {"zero_cost_policy_confirmed": False, "paid_compute_approved": False, "execution_allowed": False}, checks
    if not isinstance(evidence, dict):
        add_check(checks, "policy_evidence_object", False, type(evidence).__name__)
        return {"zero_cost_policy_confirmed": False, "paid_compute_approved": False, "execution_allowed": False}, checks

    evidence_type = str(evidence.get("evidence_type", ""))
    allows_modal_gpu = evidence.get("allows_modal_gpu") is True
    required_strings = ("confirmed_by", "confirmed_at", "evidence_summary")
    for key in required_strings:
        add_check(checks, f"policy_evidence_{key}", bool(str(evidence.get(key, "")).strip()), str(evidence.get(key, "")))
    add_check(
        checks,
        "policy_evidence_type",
        evidence_type in {"free_credit", "academic_grant", "explicit_paid_compute_approval"},
        evidence_type,
    )
    add_check(checks, "policy_evidence_allows_modal_gpu", allows_modal_gpu, str(evidence.get("allows_modal_gpu")))
    add_check(
        checks,
        "policy_evidence_has_gpu_budget",
        isinstance(evidence.get("max_gpu_hours"), (int, float)) and evidence.get("max_gpu_hours", 0) > 0,
        str(evidence.get("max_gpu_hours")),
    )
    if evidence_type == "explicit_paid_compute_approval":
        add_check(
            checks,
            "policy_evidence_has_spend_limit",
            isinstance(evidence.get("spend_limit_usd"), (int, float)) and evidence.get("spend_limit_usd", 0) > 0,
            str(evidence.get("spend_limit_usd")),
        )
    else:
        add_check(
            checks,
            "policy_evidence_zero_cost_no_spend",
            evidence.get("spend_limit_usd") in {0, 0.0, None},
            str(evidence.get("spend_limit_usd")),
        )

    evidence_passed = all(check["passed"] for check in checks)
    return {
        "zero_cost_policy_confirmed": evidence_passed and evidence_type in {"free_credit", "academic_grant"},
        "paid_compute_approved": evidence_passed and evidence_type == "explicit_paid_compute_approval",
        "execution_allowed": evidence_passed,
        "policy_evidence_type": evidence_type if evidence_passed else None,
    }, checks


def build_policy_report(
    billing_path: Path,
    preflight_path: Path,
    dry_run_path: Path,
    policy_evidence_path: Path | None = DEFAULT_POLICY_EVIDENCE,
    *,
    zero_cost_policy_confirmed: bool = False,
    paid_compute_approved: bool = False,
) -> dict[str, Any]:
    billing = load_optional_json(billing_path)
    preflight = load_optional_json(preflight_path)
    dry_run = load_optional_json(dry_run_path)
    evidence = load_optional_json(policy_evidence_path) if policy_evidence_path is not None else None
    status = modal_status(preflight)
    current_month_rows = billing if isinstance(billing, list) else None
    checks: list[dict[str, Any]] = []
    evidence_state, evidence_checks = validate_policy_evidence(evidence)

    add_check(checks, "billing_report_present", billing is not None, str(billing_path))
    add_check(checks, "billing_report_is_list", isinstance(billing, list), type(billing).__name__ if billing is not None else "missing")
    add_check(
        checks,
        "empty_billing_is_only_usage_evidence",
        current_month_rows == [],
        "empty current-month usage rows are not free credit or grant proof",
    )
    add_check(
        checks,
        "modal_preflight_policy_gate_present",
        status == "prepared-needs-credit-and-gpu-policy-check",
        status,
    )
    add_check(
        checks,
        "dry_run_present",
        isinstance(dry_run, dict) and dry_run.get("status") == "dry-run",
        str(dry_run_path),
    )
    add_check(
        checks,
        "dry_run_did_not_execute",
        isinstance(dry_run, dict) and dry_run.get("execute") is False,
        str(dry_run.get("execute") if isinstance(dry_run, dict) else "missing"),
    )
    add_check(
        checks,
        "dry_run_has_no_zero_cost_confirmation",
        isinstance(dry_run, dict) and dry_run.get("confirm_zero_cost_compute") is False,
        str(dry_run.get("confirm_zero_cost_compute") if isinstance(dry_run, dict) else "missing"),
    )
    checks.extend(evidence_checks)

    zero_cost_policy_confirmed = bool(zero_cost_policy_confirmed or evidence_state["zero_cost_policy_confirmed"])
    paid_compute_approved = bool(paid_compute_approved or evidence_state["paid_compute_approved"])
    execution_allowed = bool(zero_cost_policy_confirmed or paid_compute_approved)
    promotion_allowed = False
    return {
        "status": (
            "ready-needs-explicit-run-approval"
            if all(check["passed"] for check in checks) and execution_allowed
            else "blocked-needs-zero-cost-policy"
            if all(check["passed"] for check in checks)
            else "fail"
        ),
        "backend": "modal",
        "billing_report": str(billing_path),
        "preflight_report": str(preflight_path),
        "dry_run_report": str(dry_run_path),
        "policy_evidence_report": str(policy_evidence_path) if policy_evidence_path is not None else None,
        "policy_evidence_type": evidence_state.get("policy_evidence_type"),
        "current_month_usage_rows": len(current_month_rows) if isinstance(current_month_rows, list) else None,
        "zero_cost_policy_confirmed": zero_cost_policy_confirmed,
        "paid_compute_approved": paid_compute_approved,
        "execution_allowed": execution_allowed,
        "promotion_allowed": promotion_allowed,
        "required_gates": [
            "free credit/grant proof or explicit paid-compute approval",
            "explicit Modal run approval",
            "post-run Modal result ingest validation",
        ],
        "claim_boundary": (
            "An empty Modal billing report proves no current-month usage rows only. "
            "It does not prove free GPU credits, grant allowance, or accepted GPU policy."
        ),
        "checks": checks,
    }


def validate_policy_report(report: dict[str, Any]) -> tuple[bool, list[str]]:
    failures: list[str] = []
    execution_allowed = report.get("execution_allowed") is True
    if report.get("backend") != "modal":
        failures.append("backend must be modal")
    if execution_allowed:
        if report.get("status") != "ready-needs-explicit-run-approval":
            failures.append("execution_allowed reports must wait at ready-needs-explicit-run-approval")
        if not (report.get("zero_cost_policy_confirmed") is True or report.get("paid_compute_approved") is True):
            failures.append("execution_allowed requires zero-cost proof or explicit paid-compute approval")
        if not report.get("policy_evidence_type"):
            failures.append("execution_allowed requires a policy_evidence_type")
    else:
        if report.get("status") != "blocked-needs-zero-cost-policy":
            failures.append("status must remain blocked-needs-zero-cost-policy until policy evidence is recorded")
        if report.get("zero_cost_policy_confirmed") is not False:
            failures.append("zero_cost_policy_confirmed must be false without external policy evidence")
        if report.get("paid_compute_approved") is not False:
            failures.append("paid_compute_approved must be false without explicit approval")
    if report.get("promotion_allowed") is not False:
        failures.append("promotion_allowed must be false before scored result ingest")
    if "empty Modal billing report" not in str(report.get("claim_boundary", "")):
        failures.append("claim boundary must state that empty billing is not zero-cost proof")
    for check in report.get("checks", []):
        if not isinstance(check, dict) or check.get("passed") is not True:
            failures.append(f"failed check: {check}")
    return not failures, failures


def render_markdown(report: dict[str, Any], failures: list[str]) -> str:
    lines = [
        "# Modal Zero-Cost Policy Gate",
        "",
        f"Status: `{report['status']}`",
        f"Execution allowed: `{report['execution_allowed']}`",
        f"Promotion allowed: `{report['promotion_allowed']}`",
        f"Zero-cost policy confirmed: `{report['zero_cost_policy_confirmed']}`",
        f"Paid compute approved: `{report['paid_compute_approved']}`",
        "",
        "## Boundary",
        "",
        report["claim_boundary"],
        "",
        "## Required Gates",
        "",
    ]
    lines.extend(f"- {gate}" for gate in report["required_gates"])
    lines.extend(["", "## Checks", "", "| Check | Result | Detail |", "|---|---|---|"])
    for check in report["checks"]:
        result = "pass" if check["passed"] else "fail"
        lines.append(f"| `{check['name']}` | `{result}` | {check['detail']} |")
    if failures:
        lines.extend(["", "## Validation Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--billing-report", type=Path, default=DEFAULT_BILLING)
    parser.add_argument("--preflight-report", type=Path, default=DEFAULT_PREFLIGHT)
    parser.add_argument("--dry-run-report", type=Path, default=DEFAULT_DRY_RUN)
    parser.add_argument("--policy-evidence", type=Path, default=DEFAULT_POLICY_EVIDENCE)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    report = build_policy_report(args.billing_report, args.preflight_report, args.dry_run_report, args.policy_evidence)
    passed, failures = validate_policy_report(report)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report, failures), encoding="utf-8")
    print(json.dumps({"passed": passed, "failures": failures, "report": report}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
