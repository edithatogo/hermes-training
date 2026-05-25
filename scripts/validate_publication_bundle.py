#!/usr/bin/env python3
"""Validate a small publication evidence bundle without publishing it."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REQUIRED_FILES = (
    "run-card.md",
    "publish-readiness-checklist.md",
    "hf-model-card-draft.md",
    "license-review.md",
    "dataset-overlap-audit.json",
    "dataset-token-audit.json",
    "dataset-source-audit.json",
    "redistribution-review.md",
    "release-decision.md",
)

PUBLIC_RELEASE_GATES = (
    "Dataset/source redistribution review complete for all materialized training rows.",
    "Standard benchmark stage target is met.",
    "Hugging Face model card finalized.",
    "Human publication approval recorded.",
)

LOCAL_QUALITY_GATES = (
    "Held-out strict local tool-call suite passes at `1.000`.",
    "Mirrored regression suite passes at `1.000`.",
    "Runtime condition recorded: `/no_think` plus assistant prefill.",
)

CHECKBOX_RE = re.compile(r"^\s*-\s+\[(?P<mark>[ xX])\]\s+(?P<label>.+?)\s*$")


@dataclass(frozen=True)
class BundleStatus:
    bundle: Path
    status: str
    missing_files: tuple[str, ...]
    checked_public_release_gates: tuple[str, ...]
    unchecked_public_release_gates: tuple[str, ...]
    checked_local_quality_gates: tuple[str, ...]
    unchecked_local_quality_gates: tuple[str, ...]

    @property
    def public_ready(self) -> bool:
        return not self.missing_files and not self.unchecked_public_release_gates

    @property
    def local_quality_ready(self) -> bool:
        return not self.unchecked_local_quality_gates


def parse_checklist(path: Path) -> dict[str, bool]:
    items: dict[str, bool] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = CHECKBOX_RE.match(line)
        if match:
            items[match.group("label")] = match.group("mark").lower() == "x"
    return items


def evaluate_bundle(bundle: Path, required_files: tuple[str, ...] = DEFAULT_REQUIRED_FILES) -> BundleStatus:
    missing = tuple(rel for rel in required_files if not (bundle / rel).exists())
    checklist = bundle / "publish-readiness-checklist.md"
    items = parse_checklist(checklist) if checklist.exists() else {}

    checked_public = tuple(gate for gate in PUBLIC_RELEASE_GATES if items.get(gate, False))
    unchecked_public = tuple(gate for gate in PUBLIC_RELEASE_GATES if not items.get(gate, False))
    checked_quality = tuple(gate for gate in LOCAL_QUALITY_GATES if items.get(gate, False))
    unchecked_quality = tuple(gate for gate in LOCAL_QUALITY_GATES if not items.get(gate, False))

    if missing:
        status = "invalid"
    elif unchecked_public:
        status = "blocked"
    else:
        status = "ready"

    return BundleStatus(
        bundle=bundle,
        status=status,
        missing_files=missing,
        checked_public_release_gates=checked_public,
        unchecked_public_release_gates=unchecked_public,
        checked_local_quality_gates=checked_quality,
        unchecked_local_quality_gates=unchecked_quality,
    )


def status_to_dict(status: BundleStatus) -> dict[str, object]:
    return {
        "bundle": str(status.bundle),
        "status": status.status,
        "public_ready": status.public_ready,
        "local_quality_ready": status.local_quality_ready,
        "missing_files": list(status.missing_files),
        "checked_public_release_gates": list(status.checked_public_release_gates),
        "unchecked_public_release_gates": list(status.unchecked_public_release_gates),
        "checked_local_quality_gates": list(status.checked_local_quality_gates),
        "unchecked_local_quality_gates": list(status.unchecked_local_quality_gates),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="Publication bundle directory.")
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="Fail unless all public release gates are complete.",
    )
    parser.add_argument(
        "--expect-blocked",
        action="store_true",
        help="Fail unless the bundle is intentionally blocked for public release.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable status.")
    args = parser.parse_args()

    status = evaluate_bundle(args.bundle)
    data = status_to_dict(status)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"bundle: {status.bundle}")
        print(f"status: {status.status}")
        print(f"public_ready: {status.public_ready}")
        print(f"local_quality_ready: {status.local_quality_ready}")
        if status.missing_files:
            print("missing_files:")
            for rel in status.missing_files:
                print(f"- {rel}")
        if status.unchecked_public_release_gates:
            print("unchecked_public_release_gates:")
            for gate in status.unchecked_public_release_gates:
                print(f"- {gate}")

    if status.missing_files:
        return 1
    if status.unchecked_local_quality_gates:
        return 1
    if args.require_ready and not status.public_ready:
        return 1
    if args.expect_blocked and status.status != "blocked":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
