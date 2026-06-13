#!/usr/bin/env python3
"""Build the prompt/profile repair queue for strict-format-blocked Hermes candidates."""
from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = ROOT / "MODEL_CANDIDATES.yaml"
DEFAULT_COVERAGE = ROOT / "reports/benchmark/coverage/all-candidate-benchmark-coverage-20260612.json"
DEFAULT_OUTPUT = ROOT / "reports/benchmark/coverage/prompt-profile-repair-queue-20260614"
REPAIR_REASONS = (
    "blocked by strict Hermes tool-call formatting failure",
    "blocked by empty/no-content generation under the strict prompt",
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parameter_order(parameters: str) -> tuple[int, str]:
    numbers = [float(match) for match in re.findall(r"(\d+(?:\.\d+)?)\s*b", parameters.lower())]
    size = min(numbers) if numbers else 999.0
    if size <= 2:
        return 0, "tiny"
    if size <= 4:
        return 1, "small"
    if size <= 9:
        return 2, "medium"
    if size <= 14:
        return 3, "large-local"
    return 4, "oversized-local-or-cloud"


def repair_hypothesis(candidate: dict[str, Any], blocked_reason: str) -> str:
    text = " ".join(str(candidate.get(key, "")) for key in ("id", "family", "notes", "first_runtime")).lower()
    if "empty/no-content" in blocked_reason:
        return "retry only after a prompt profile changes prefill, stop tokens, or thinking/no-thinking controls"
    if "gemma" in text:
        return "test Gemma native tool-fragment normalization or a stricter system suffix without changing raw outputs"
    if "granite" in text:
        return "test Granite native tool-call normalization and copy-exact argument constraints"
    if "minicpm" in text:
        return "test MiniCPM tool-tag extraction only as score-only analysis before any helper promotion"
    if "lfm" in text:
        return "test refusal wording and strict JSON/tool envelope profile on the existing GGUF endpoint"
    if "exaone" in text:
        return "test strict JSON envelope prompting on the existing GGUF endpoint; keep MLX blocked until loader support changes"
    if "qwen" in text:
        return "test Qwen-style no-think/prefill controls and strict forbidden-tool wording"
    return "design a model-family-specific runtime profile, then rerun the strict BFCL pilot with no-extra-tool-text scoring"


def command_for(candidate: dict[str, Any]) -> str:
    model_id = str(candidate.get("id", ""))
    environment = str(candidate.get("environment", ""))
    slug = slugify(model_id)
    if "gguf" in model_id.lower() or environment in {"mac-lmstudio", "mac-ollama"}:
        return "\n".join(
            [
                "source scripts/env.sh",
                "# No download here: start the existing local endpoint for this artifact, then rerun after a prompt/profile change.",
                "./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \\",
                f"  --model {slug} \\",
                "  --base-url http://127.0.0.1:<port>/v1 \\",
                "  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \\",
                "  --require-no-extra-tool-text \\",
                f"  --run-id {slug}-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    return "\n".join(
        [
            "source scripts/env.sh",
            "# No download here: use the SSD cache/local artifact already proven for this candidate.",
            "./.venv/bin/python scripts/run_local_pilot_benchmark.py \\",
            f"  --model {model_id} \\",
            "  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \\",
            "  --require-no-extra-tool-text \\",
            f"  --run-id {slug}-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)",
        ]
    )


def build_rows(candidates: list[dict[str, Any]], coverage_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {str(candidate.get("id")): candidate for candidate in candidates}
    rows: list[dict[str, Any]] = []
    for coverage in coverage_rows:
        if coverage.get("project") != "hermes":
            continue
        blocked_reason = str(coverage.get("blocked_reason", ""))
        if blocked_reason not in REPAIR_REASONS:
            continue
        candidate_id = str(coverage.get("id", ""))
        candidate = by_id.get(candidate_id, {})
        _, size_bucket = parameter_order(str(candidate.get("parameters", "")))
        rows.append(
            {
                "id": candidate_id,
                "family": candidate.get("family", coverage.get("family", "")),
                "role": candidate.get("role", coverage.get("role", "")),
                "environment": candidate.get("environment", coverage.get("environment_or_runtime", "")),
                "parameters": candidate.get("parameters", ""),
                "size_bucket": size_bucket,
                "coverage_state": coverage.get("coverage_state", ""),
                "blocked_reason": blocked_reason,
                "repair_hypothesis": repair_hypothesis(candidate, blocked_reason),
                "evidence": coverage.get("evidence", []),
                "next_command": command_for(candidate or {"id": candidate_id, "environment": coverage.get("environment_or_runtime", "")}),
                "promotion_boundary": "Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.",
            }
        )
    rows.sort(key=lambda row: (parameter_order(str(row["parameters"]))[0], str(row["family"]), str(row["id"])))
    return rows


def render_markdown(rows: list[dict[str, Any]], run_id: str, created_at: str) -> str:
    lines = [
        "# Prompt/Profile Repair Queue",
        "",
        f"Run ID: `{run_id}`",
        f"Created: `{created_at}`",
        "",
        "Purpose: isolate runtime-proven or partially proven Hermes candidates whose next local work is prompt/profile repair, not training or remote execution.",
        "",
        "## Queue",
        "",
        "| Priority | Candidate | Params | Environment | Blocker | Repair hypothesis |",
        "|---:|---|---|---|---|---|",
    ]
    for index, row in enumerate(rows, 1):
        lines.append(
            f"| {index} | `{row['id']}` | {row['parameters'] or 'unknown'} | `{row['environment']}` | {row['blocked_reason']} | {row['repair_hypothesis']} |"
        )
    lines.extend(["", "## Command Templates", ""])
    for row in rows[:12]:
        lines.extend(
            [
                f"### {row['id']}",
                "",
                f"- Evidence: {', '.join(f'`{item}`' for item in row.get('evidence', [])) or 'none recorded'}",
                f"- Boundary: {row['promotion_boundary']}",
                "",
                "```bash",
                str(row["next_command"]),
                "```",
                "",
            ]
        )
    lines.extend(
        [
            "## Policy",
            "",
            "- Do not redownload models for this queue; use existing SSD-backed artifacts or endpoints.",
            "- Do not treat score-only normalizers as promotion evidence.",
            "- Keep raw responses and normalized-for-score responses distinct in future reports.",
            "- Keep strict `--require-no-extra-tool-text` scoring for Hermes tool-call claims.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    parser.add_argument("--output-stem", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--created-at")
    args = parser.parse_args()

    candidates = load_yaml(args.candidates).get("candidates", [])
    coverage_rows = load_json(args.coverage).get("rows", [])
    if not isinstance(candidates, list) or not isinstance(coverage_rows, list):
        raise ValueError("candidate and coverage inputs must contain lists")
    rows = build_rows([item for item in candidates if isinstance(item, dict)], coverage_rows)
    run_id = args.output_stem.name
    created_at = args.created_at or datetime.now(UTC).isoformat()
    payload = {
        "run_id": run_id,
        "created_at": created_at,
        "source_candidates": str(args.candidates),
        "source_coverage": str(args.coverage),
        "rows": rows,
    }
    args.output_stem.parent.mkdir(parents=True, exist_ok=True)
    json_path = args.output_stem.with_suffix(".json")
    md_path = args.output_stem.with_suffix(".md")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(rows, run_id, created_at), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path), "rows": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
