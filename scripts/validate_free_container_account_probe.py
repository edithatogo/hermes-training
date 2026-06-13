#!/usr/bin/env python3
"""Validate the free-container account probe report keeps its safety boundary."""
from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "reports" / "cloud" / "free-container-account-probe-20260613.md"

REQUIRED_TEXT = (
    "without launching jobs, creating resources, uploading artifacts, or using paid compute",
    "## Modal",
    "Auth state: authenticated",
    "Remaining gates:",
    "## Kaggle",
    "Auth state: authenticated",
    "GPU quota",
    "## Lightning AI",
    "Teamspace owner error",
    "## Current Decision",
)
FORBIDDEN_TEXT = (
    "super-secret-token",
    "HF_TOKEN=",
    "KAGGLE_KEY=",
    "modal run ",
    "lightning run ",
    "lightning job create",
)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_report(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {display_path(path)}"]
    text = path.read_text(encoding="utf-8")
    normalized = " ".join(text.split())
    for needle in REQUIRED_TEXT:
        if needle not in normalized:
            failures.append(f"{display_path(path)} missing required text: {needle}")
    lowered = text.lower()
    for needle in FORBIDDEN_TEXT:
        if needle.lower() in lowered:
            failures.append(f"{display_path(path)} contains forbidden text: {needle}")
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures = validate_report(args.report)
    if failures:
        print("not ready: free-container account probe")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: free-container account probe is safe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
