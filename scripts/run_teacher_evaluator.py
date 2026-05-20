#!/usr/bin/env python3
"""Azure teacher/evaluator job entrypoint.

This is a fail-closed skeleton. It records run metadata but does not create
judge labels or quality claims until a real evaluator is wired in.
"""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference_model", required=True)
    parser.add_argument("--candidate_model", required=True)
    parser.add_argument("--task_set", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Write skeleton metadata only instead of running a real evaluator.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "created_at": datetime.now(UTC).isoformat(),
        "reference_model": args.reference_model,
        "candidate_model": args.candidate_model,
        "task_set": args.task_set,
        "dry_run": args.dry_run,
        "status": "skeleton-only",
        "judgements": [],
        "notes": "No teacher labels produced. Wire evaluator prompts and human spot checks before promotion.",
    }
    (output_dir / "teacher_evaluator_skeleton.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
