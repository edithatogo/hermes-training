#!/usr/bin/env python3
"""Inspect Azure readiness for Hermes scale-out work without creating resources."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_ACCOUNT = "d.a.mordaunt@gmail.com"
DEFAULT_SUBSCRIPTION = "Azure for Students"
DEFAULT_STORAGE_ROOT = Path("/Volumes/PortableSSD")


def run_az(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(["az", *args], capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def print_check(label: str, passed: bool, detail: str) -> None:
    status = "ok" if passed else "fail"
    print(f"{status}: {label}: {detail}")


def load_json_or_none(stdout: str) -> object | None:
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-account", default=DEFAULT_ACCOUNT)
    parser.add_argument("--expected-subscription", default=DEFAULT_SUBSCRIPTION)
    parser.add_argument("--storage-root", default=str(DEFAULT_STORAGE_ROOT))
    parser.add_argument("--region", default="australiaeast")
    parser.add_argument(
        "--check-quota",
        action="store_true",
        help="Also inspect regional VM quota. This is read-only and does not create compute.",
    )
    args = parser.parse_args()

    failures: list[str] = []

    az_path = shutil.which("az")
    print_check("azure cli", bool(az_path), az_path or "not found")
    if not az_path:
        return 1

    code, stdout, stderr = run_az(["account", "show", "--output", "json"])
    account = load_json_or_none(stdout) if code == 0 else None
    if not isinstance(account, dict):
        print_check("active account", False, stderr or stdout or "not logged in")
        failures.append("active account")
    else:
        user = (account.get("user") or {}).get("name", "")
        subscription = str(account.get("name", ""))
        state = str(account.get("state", ""))
        print_check("active user", user.lower() == args.expected_account.lower(), user)
        print_check("subscription name", subscription == args.expected_subscription, subscription)
        print_check("subscription enabled", state == "Enabled", state)
        if user.lower() != args.expected_account.lower():
            failures.append("active user")
        if subscription != args.expected_subscription:
            failures.append("subscription name")
        if state != "Enabled":
            failures.append("subscription enabled")

    code, stdout, stderr = run_az(["extension", "list", "--output", "json"])
    extensions = load_json_or_none(stdout) if code == 0 else None
    has_ml = isinstance(extensions, list) and any(ext.get("name") == "ml" for ext in extensions)
    print_check("azure ml cli extension", has_ml, "installed" if has_ml else "missing")
    if not has_ml:
        failures.append("azure ml cli extension")

    storage_root = Path(args.storage_root)
    print_check("ssd artifact root", storage_root.exists(), str(storage_root))
    if not storage_root.exists():
        failures.append("ssd artifact root")

    print("info: region:", args.region)
    print("info: cost policy: spot/low-priority, max_instances=1, min_instances=0")
    print("info: this preflight does not create compute or submit jobs")

    if args.check_quota and not failures:
        code, stdout, stderr = run_az(["vm", "list-usage", "--location", args.region, "--output", "json"])
        usages = load_json_or_none(stdout) if code == 0 else None
        if not isinstance(usages, list):
            print_check("regional quota", False, stderr or stdout or "unable to read usage")
            failures.append("regional quota")
        else:
            interesting = []
            for item in usages:
                raw = str((item.get("name") or {}).get("value", ""))
                label = str((item.get("name") or {}).get("localizedValue", ""))
                haystack = f"{raw} {label}".lower()
                if re.search(r"\bstandard\s+n[cdgvps]", haystack) or "gpu" in haystack:
                    interesting.append(item)
            if interesting:
                print("info: quota candidates:")
                for item in interesting:
                    name = (item.get("name") or {}).get("localizedValue") or (item.get("name") or {}).get("value")
                    print(f"- {name}: current={item.get('currentValue')} limit={item.get('limit')}")
            else:
                print("info: regional quota: no GPU-family usage rows matched; inspect Azure ML quota in portal if needed")

    if failures:
        print("\nnot ready:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("\nready: Azure account preflight passed; quota checks still required before compute")
    return 0


if __name__ == "__main__":
    sys.exit(main())
