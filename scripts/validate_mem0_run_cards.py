#!/usr/bin/env python3
"""Validate mem0 run-card coverage for benchmark index rows."""
from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "reports/benchmark/mem0/index.md"
DEFAULT_RUN_CARD_DIR = ROOT / "reports/benchmark/mem0/run-cards"
REQUIRED_HEADINGS = ("## Candidate", "## Command", "## Result", "## Decision")


def parse_index_rows(index_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| Kind | Run ID |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            break
        if line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 10:
            continue
        output = cells[9]
        if output.startswith("`") and output.endswith("`"):
            output = output[1:-1]
        rows.append({"kind": cells[0], "run_id": cells[1], "output": output})
    return rows


def validate_run_card(card_path: Path, row: dict[str, str]) -> list[str]:
    failures: list[str] = []
    if not card_path.exists():
        return [f"missing run card for {row['run_id']}: {display_path(card_path)}"]

    text = card_path.read_text(encoding="utf-8")
    if f"Run ID: {row['run_id']}" not in text:
        failures.append(f"{display_path(card_path)} does not declare Run ID: {row['run_id']}")
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            failures.append(f"{display_path(card_path)} missing {heading}")

    summary_line = next((line for line in text.splitlines() if line.startswith("Summary: `")), "")
    if not summary_line:
        failures.append(f"{display_path(card_path)} missing Summary path")
    else:
        summary_path = Path(summary_line.split("`")[1])
        if not summary_path.exists():
            failures.append(f"{display_path(card_path)} summary does not exist: {summary_path}")
        expected_output = row.get("output")
        if expected_output:
            expected_summary = Path(expected_output) / "summary.json"
            if summary_path != expected_summary:
                failures.append(
                    f"{display_path(card_path)} summary path {summary_path} does not match index output {expected_summary}"
                )
    return failures


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--run-card-dir", type=Path, default=DEFAULT_RUN_CARD_DIR)
    args = parser.parse_args()

    if not args.index.exists():
        print(f"not ready: missing {display_path(args.index)}")
        return 1
    rows = parse_index_rows(args.index)
    if not rows:
        print(f"not ready: {display_path(args.index)} has no benchmark rows")
        return 1

    failures: list[str] = []
    seen: set[str] = set()
    for row in rows:
        run_id = row["run_id"]
        if run_id in seen:
            failures.append(f"duplicate index run id: {run_id}")
            continue
        seen.add(run_id)
        failures.extend(validate_run_card(args.run_card_dir / f"{run_id}.md", row))

    if failures:
        print("not ready: mem0 run cards")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"ready: mem0 run cards cover {len(rows)} indexed runs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
