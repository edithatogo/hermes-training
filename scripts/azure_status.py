#!/usr/bin/env python3
"""Read-only Azure status report for Hermes scale-out readiness."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


PROVIDERS = (
    "Microsoft.MachineLearningServices",
    "Microsoft.Compute",
    "Microsoft.Storage",
    "Microsoft.KeyVault",
    "Microsoft.ContainerRegistry",
    "Microsoft.Insights",
)


def az(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(["az", *args], capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main() -> int:
    if not shutil.which("az"):
        print("fail: Azure CLI not found")
        return 1

    code, stdout, stderr = az(["account", "show", "-o", "json"])
    if code:
        print(f"fail: account: {stderr or stdout}")
        return 1
    account = json.loads(stdout)
    print("account:")
    print(f"- user: {(account.get('user') or {}).get('name')}")
    print(f"- subscription: {account.get('name')}")
    print(f"- state: {account.get('state')}")
    print(f"- tenant: {account.get('tenantDisplayName') or account.get('tenantId')}")

    print("\nproviders:")
    for provider in PROVIDERS:
        code, stdout, stderr = az(["provider", "show", "-n", provider, "--query", "registrationState", "-o", "tsv"])
        state = stdout if code == 0 else f"error: {stderr or stdout}"
        print(f"- {provider}: {state}")

    print("\nresource groups:")
    code, stdout, stderr = az(["group", "list", "-o", "json"])
    if code:
        print(f"- error: {stderr or stdout}")
    else:
        for group in json.loads(stdout):
            print(f"- {group.get('name')} ({group.get('location')}) {group.get('properties', {}).get('provisioningState')}")

    print("\nazure ml workspaces:")
    code, stdout, stderr = az(["ml", "workspace", "list", "-o", "json"])
    if code:
        print(f"- error: {stderr or stdout}")
    else:
        workspaces = json.loads(stdout)
        if not workspaces:
            print("- none")
        for workspace in workspaces:
            print(f"- {workspace.get('name')} ({workspace.get('location')}) rg={workspace.get('resourceGroup')}")

    template_root = Path("templates/azure")
    print("\ntemplates:")
    for path in sorted(template_root.glob("*.yaml")):
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
