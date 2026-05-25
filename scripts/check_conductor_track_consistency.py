#!/usr/bin/env python3
"""Validate Conductor track registry, metadata, and plan status alignment."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMPLETE_STATUSES = {"complete", "completed"}
OPEN_STATUSES = {"new", "planned", "in_progress", "in-progress", "active"}


@dataclass(frozen=True)
class RegistryTrack:
    title: str
    marker: str
    path: Path

    @property
    def completed(self) -> bool:
        return self.marker.lower() == "x"


def parse_registry(root: Path) -> list[RegistryTrack]:
    registry = root / "conductor" / "tracks.md"
    text = registry.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^## \[(?P<marker>[ xX~])\] Track: (?P<title>.+?)\n"
        r"\*Link: \[(?P<label>[^\]]+)\]\((?P<link>\./tracks/[^)]+)\)\*",
        flags=re.MULTILINE,
    )
    tracks: list[RegistryTrack] = []
    for match in pattern.finditer(text):
        link = match.group("link").removeprefix("./")
        tracks.append(
            RegistryTrack(
                title=match.group("title").strip(),
                marker=match.group("marker").strip(),
                path=root / "conductor" / link,
            )
        )
    return tracks


def load_metadata(path: Path) -> dict[str, Any]:
    metadata_path = path / "metadata.json"
    with metadata_path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{metadata_path}: expected JSON object")
    return data


def unchecked_plan_items(path: Path) -> list[str]:
    plan_path = path / "plan.md"
    if not plan_path.exists():
        return []
    items: list[str] = []
    for line in plan_path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\s*-\s+\[\s\]\s+", line):
            items.append(line.strip())
    return items


def validate(root: Path) -> list[str]:
    failures: list[str] = []
    tracks = parse_registry(root)
    if not tracks:
        return ["conductor/tracks.md: no track entries parsed"]

    for track in tracks:
        rel = track.path.relative_to(root)
        if not track.path.exists():
            failures.append(f"{rel}: registry link target is missing")
            continue
        metadata_path = track.path / "metadata.json"
        if not metadata_path.exists():
            failures.append(f"{metadata_path.relative_to(root)}: metadata.json is missing")
            continue
        metadata = load_metadata(track.path)
        status = str(metadata.get("status", "")).lower()
        if track.completed and status not in COMPLETE_STATUSES:
            failures.append(
                f"{metadata_path.relative_to(root)}: registry is complete but metadata status is {status or '<missing>'}"
            )
        if not track.completed and status in COMPLETE_STATUSES:
            failures.append(
                f"{metadata_path.relative_to(root)}: registry is open but metadata status is {status}"
            )
        if track.completed:
            for item in unchecked_plan_items(track.path):
                failures.append(f"{(track.path / 'plan.md').relative_to(root)}: completed registry has unchecked item: {item}")
        elif status in OPEN_STATUSES:
            continue

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    failures = validate(args.root.resolve())
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    print("Conductor track registry, metadata, and plan statuses are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
