#!/usr/bin/env python3
"""Azure benchmark job entrypoint.

This is a fail-closed skeleton. It writes run metadata for smoke/template
validation, but it does not claim benchmark scores. Replace the dry-run guard
only when the benchmark harness is installed in the target Azure ML environment.
"""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model_id", required=True)
    parser.add_argument("--suite", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Write skeleton metadata only instead of running a real benchmark.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "created_at": datetime.now(UTC).isoformat(),
        "model_id": args.model_id,
        "suite": args.suite,
        "dry_run": args.dry_run,
        "status": "skeleton-only",
        "scores": {},
        "notes": "No benchmark scores produced. Wire lm-eval/BFCL/coding harness before promotion.",
    }
    (output_dir / "benchmark_skeleton.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
