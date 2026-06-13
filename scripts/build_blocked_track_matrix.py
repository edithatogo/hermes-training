#!/usr/bin/env python3
"""Generate a matrix of active blocked Conductor tracks and unblock gates."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACKS = ROOT / "conductor/tracks.md"
DEFAULT_CHECKLIST = ROOT / "reports/cloud/backend-unblock-checklist-20260613.json"
DEFAULT_MARKDOWN = ROOT / "reports/cloud/active-blocked-track-matrix-20260613.md"
DEFAULT_JSON = ROOT / "reports/cloud/active-blocked-track-matrix-20260613.json"

TRACK_RE = re.compile(r"^## \[(?P<marker>[ x~])\] Track: (?P<title>.+)$")
LINK_RE = re.compile(r"\*Link: \[(?P<label>[^\]]+)\]\((?P<link>[^)]+)\)\*")


@dataclass(frozen=True)
class RegistryTrack:
    title: str
    marker: str
    path: Path


def parse_registry(path: Path) -> list[RegistryTrack]:
    lines = path.read_text(encoding="utf-8").splitlines()
    tracks: list[RegistryTrack] = []
    index = 0
    while index < len(lines):
        match = TRACK_RE.match(lines[index])
        if not match:
            index += 1
            continue
        title = match.group("title")
        marker = match.group("marker")
        link = ""
        if index + 1 < len(lines):
            link_match = LINK_RE.match(lines[index + 1])
            if link_match:
                link = link_match.group("link")
        if link.startswith("./"):
            track_path = (path.parent / link[2:]).resolve()
        else:
            track_path = (path.parent / link).resolve()
        tracks.append(RegistryTrack(title=title, marker=marker, path=track_path))
        index += 2
    return tracks


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_unblock_items(path: Path) -> dict[str, dict[str, Any]]:
    data = load_json(path)
    items = data.get("items", [])
    if not isinstance(items, list):
        raise ValueError(f"{path} items must be a list")
    return {str(item["backend"]): item for item in items if isinstance(item, dict) and "backend" in item}


def backend_for_track(track_id: str, title: str) -> str:
    haystack = f"{track_id} {title}".lower()
    if "hf-jobs" in haystack or "hf jobs" in haystack:
        return "hf_jobs"
    if "kaggle" in haystack:
        return "kaggle"
    if "ngc" in haystack:
        return "ngc"
    if "azure" in haystack:
        return "azure"
    if "colab" in haystack:
        return "colab"
    return "unknown"


def first_unchecked_task(plan_path: Path) -> str:
    if not plan_path.exists():
        return ""
    lines = plan_path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("- [ ] Task:"):
            task = stripped.removeprefix("- [ ] Task:").strip()
            cursor = index + 1
            while cursor < len(lines):
                continuation = lines[cursor]
                stripped_continuation = continuation.strip()
                if not continuation.startswith("  ") or stripped_continuation.startswith("- ["):
                    break
                if stripped_continuation:
                    task = f"{task} {stripped_continuation}"
                cursor += 1
            return task
    return ""


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def build_rows(registry_path: Path, checklist_path: Path) -> list[dict[str, Any]]:
    unblock_items = load_unblock_items(checklist_path)
    rows: list[dict[str, Any]] = []
    for track in parse_registry(registry_path):
        metadata_path = track.path / "metadata.json"
        if not metadata_path.exists():
            continue
        metadata = load_json(metadata_path)
        if metadata.get("status") != "blocked":
            continue
        track_id = str(metadata.get("track_id") or track.path.name)
        backend = backend_for_track(track_id, track.title)
        unblock = unblock_items.get(backend, {})
        rows.append(
            {
                "track_id": track_id,
                "title": track.title,
                "backend": backend,
                "backend_status": unblock.get("status", "unknown"),
                "blocker": unblock.get("blocker", "No backend-specific unblock checklist entry."),
                "next_task": first_unchecked_task(track.path / "plan.md"),
                "track_path": display_path(track.path),
                "commands": unblock.get("commands", []),
            }
        )
    rows.sort(key=lambda row: (str(row["backend"]), str(row["track_id"])))
    return rows


def render_markdown(rows: list[dict[str, Any]], registry_path: Path, checklist_path: Path) -> str:
    lines = [
        "# Active Blocked Track Matrix",
        "",
        f"Registry: `{display_path(registry_path)}`",
        f"Unblock checklist: `{display_path(checklist_path)}`",
        "",
        "| Track | Backend | Backend status | Blocker | Next unchecked task |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| `{track_id}` | `{backend}` | `{backend_status}` | {blocker} | {next_task} |".format(
                track_id=row["track_id"],
                backend=row["backend"],
                backend_status=row["backend_status"],
                blocker=row["blocker"],
                next_task=row["next_task"] or "No unchecked task recorded.",
            )
        )
    lines.append("")
    lines.append("## Commands")
    lines.append("")
    for row in rows:
        commands = row.get("commands") or []
        if not commands:
            continue
        lines.append(f"### {row['track_id']}")
        lines.append("")
        lines.append("```bash")
        lines.extend(str(command) for command in commands)
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_TRACKS)
    parser.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    args = parser.parse_args()

    rows = build_rows(args.registry, args.checklist)
    payload = {
        "registry": display_path(args.registry) if args.registry.is_absolute() else str(args.registry),
        "checklist": display_path(args.checklist) if args.checklist.is_absolute() else str(args.checklist),
        "rows": rows,
    }
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text(render_markdown(rows, args.registry, args.checklist), encoding="utf-8")
    args.json_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
