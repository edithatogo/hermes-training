#!/usr/bin/env python3
"""Validate Azure execution templates without creating Azure resources."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


REQUIRED_TEMPLATES = (
    "workspace.yaml",
    "compute-lowpri-t4.yaml",
    "compute-lowpri-a100.yaml",
    "benchmark-job.yaml",
    "teacher-evaluator-job.yaml",
    "cloud-run-card.md",
)


def fail(message: str) -> None:
    print(f"fail: {message}")
    raise SystemExit(1)


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        fail(f"{path}: expected YAML object")
    return data


def assert_low_priority_compute(path: Path) -> None:
    data = load_yaml(path)
    if data.get("type") != "amlcompute":
        fail(f"{path}: expected amlcompute")
    if data.get("tier") != "low_priority":
        fail(f"{path}: compute tier must be low_priority")
    if data.get("min_instances") != 0:
        fail(f"{path}: min_instances must be 0")
    if data.get("max_instances") != 1:
        fail(f"{path}: max_instances must be 1")
    tags = data.get("tags") or {}
    if str(tags.get("max_instances")) != "1":
        fail(f"{path}: max_instances tag must be 1")
    print(f"ok: {path}: low-priority max-one compute")


def assert_job(path: Path) -> None:
    data = load_yaml(path)
    command = str(data.get("command", ""))
    if "--dry-run" not in command:
        fail(f"{path}: command must include --dry-run")
    tags = data.get("tags") or {}
    if tags.get("local_artifact_root") != "/Volumes/PortableSSD":
        fail(f"{path}: local_artifact_root tag must be /Volumes/PortableSSD")
    if str(tags.get("max_instances")) != "1":
        fail(f"{path}: max_instances tag must be 1")
    compute = str(data.get("compute", ""))
    if "precreated" not in compute:
        fail(f"{path}: compute must remain a precreated placeholder")
    outputs = data.get("outputs") or {}
    if "results" not in outputs:
        fail(f"{path}: missing results output")
    print(f"ok: {path}: fail-closed dry-run job")


def assert_workspace(path: Path, expected_owner: str) -> None:
    data = load_yaml(path)
    tags = data.get("tags") or {}
    if tags.get("owner") != expected_owner:
        fail(f"{path}: owner tag must be {expected_owner}")
    if tags.get("cost_policy") != "preflight-required":
        fail(f"{path}: cost_policy tag must be preflight-required")
    print(f"ok: {path}: gated workspace template")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template-root", type=Path, default=Path("templates/azure"))
    parser.add_argument("--expected-owner", default="d.a.mordaunt@gmail.com")
    args = parser.parse_args()

    for name in REQUIRED_TEMPLATES:
        path = args.template_root / name
        if not path.exists():
            fail(f"missing {path}")
        print(f"ok: {path}: exists")

    assert_workspace(args.template_root / "workspace.yaml", args.expected_owner)
    assert_low_priority_compute(args.template_root / "compute-lowpri-t4.yaml")
    assert_low_priority_compute(args.template_root / "compute-lowpri-a100.yaml")
    assert_job(args.template_root / "benchmark-job.yaml")
    assert_job(args.template_root / "teacher-evaluator-job.yaml")
    print("ready: Azure execution templates remain fail-closed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
