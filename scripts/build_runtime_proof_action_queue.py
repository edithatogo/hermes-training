#!/usr/bin/env python3
"""Build a prioritized runtime-proof action queue from model radar and coverage."""
from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COVERAGE = ROOT / "reports" / "benchmark" / "coverage" / "all-candidate-benchmark-coverage-20260612.json"
DEFAULT_OUTPUT = ROOT / "reports" / "benchmark" / "coverage" / "runtime-proof-action-queue-20260613"


LOCAL_ENVS = {"mac-mlx", "mac-lmstudio", "mac-ollama", "hf-transformers"}
SPECIALIST_ENVS = {"specialist-runtime"}
CLOUD_ENVS = {"azure-cuda", "hosted-api"}
SUPPORT_KEYWORDS = (
    "embedding",
    "embeddings",
    "embed",
    "reranker",
    "rerank",
    "colbert",
    "asr",
    "tts",
    "audio",
    "vl",
    "vision",
    "locateanything",
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML object")
    return data


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parameter_size_bucket(parameters: str) -> tuple[int, str]:
    text = parameters.lower()
    numbers = [float(match) for match in re.findall(r"(\d+(?:\.\d+)?)\s*b", text)]
    active_match = re.search(r"(\d+(?:\.\d+)?)\s*b\s*active", text)
    active = float(active_match.group(1)) if active_match else None
    effective = active or (min(numbers) if numbers else 999.0)
    if effective <= 2:
        return 0, "tiny"
    if effective <= 4:
        return 1, "small"
    if effective <= 9:
        return 2, "medium"
    if effective <= 14:
        return 3, "large-local"
    if effective <= 32:
        return 4, "cloud-or-quant"
    return 5, "cloud-only"


def lane_for(item: dict[str, Any], coverage_state: str, blocked_reason: str) -> str:
    env = str(item.get("environment", ""))
    role = str(item.get("role", ""))
    feasibility = str(item.get("feasibility", ""))
    searchable = " ".join(
        str(item.get(key, ""))
        for key in ("id", "family", "tier", "role", "architecture", "first_runtime", "notes")
    ).lower()
    if role == "watchlist" or feasibility in {"speculative", "hosted-preview-only"}:
        return "watchlist"
    if role == "retrieval" or any(keyword in searchable for keyword in SUPPORT_KEYWORDS):
        return "support-model-proof"
    if (
        "strict Hermes tool-call formatting failure" in blocked_reason
        or "empty/no-content generation under the strict prompt" in blocked_reason
    ):
        return "prompt-profile-repair"
    if env in LOCAL_ENVS:
        return "mac-runtime-proof"
    if env in SPECIALIST_ENVS:
        return "specialist-runtime-proof"
    if env in CLOUD_ENVS or role in {"cloud-teacher", "hosted-teacher", "cloud-finetune"}:
        return "cloud-teacher-proof"
    if coverage_state in {"smoke-or-pilot-only", "evidence-present-needs-review"}:
        return "evidence-hardening"
    return "deferred"


def next_command(item: dict[str, Any], lane: str) -> str:
    model_id = str(item.get("id", ""))
    env = str(item.get("environment", ""))
    first_runtime = str(item.get("first_runtime", ""))
    searchable = " ".join(
        str(item.get(key, ""))
        for key in ("id", "family", "tier", "role", "architecture", "first_runtime", "notes")
    ).lower()
    slug = normalize(model_id)
    if lane == "support-model-proof":
        if "jina" in searchable and "mlx" in searchable:
            task_type = "text-matching" if "text-matching" in searchable else "retrieval"
            return "\n".join(
                [
                    "source scripts/env.sh",
                    "# Use an SSD-backed cache/repo-dir and local-files-only once the artifact is acquired.",
                    "./.venv/bin/python scripts/run_jina_mlx_embedding_benchmark.py \\",
                    f"  --model {model_id} \\",
                    f"  --task-type {task_type} \\",
                    "  --repo-dir /Volumes/PortableSSD/huggingface/hub/jina-mlx/<repo-dir> \\",
                    "  --local-files-only \\",
                    "  --suite benchmarks/embeddings/memory_retrieval_differentiation_suite.json \\",
                    f"  --run-id {slug}-retrieval-proof-$(date +%Y%m%d-%H%M%S)",
                ]
            )
        if any(keyword in searchable for keyword in ("embedding", "embeddings", "embed", "bge", "qwen3-vl-reranker")):
            return "\n".join(
                [
                    "source scripts/env.sh",
                    "python -m pip install -r requirements-mem0-embeddings.txt",
                    "./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \\",
                    f"  --model {model_id} \\",
                    "  --device cpu \\",
                    "  --suite benchmarks/embeddings/memory_retrieval_differentiation_suite.json \\",
                    f"  --run-id {slug}-retrieval-proof-$(date +%Y%m%d-%H%M%S)",
                ]
            )
        return "\n".join(
            [
                "source scripts/env.sh",
                "# Run a role-specific smoke only after license/runtime checks; keep raw artifacts on /Volumes/PortableSSD.",
                "./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py",
            ]
        )
    if lane == "mac-runtime-proof" and "gguf" in (model_id + " " + first_runtime).lower():
        return "\n".join(
            [
                "source scripts/env.sh",
                "# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.",
                "./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \\",
                f"  --model {slug} \\",
                "  --base-url http://127.0.0.1:<port>/v1 \\",
                "  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \\",
                f"  --run-id {slug}-bfcl-pilot-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    if lane == "mac-runtime-proof" and env == "mac-mlx":
        return "\n".join(
            [
                "source scripts/env.sh",
                "# Acquire the MLX model to the SSD Hugging Face cache first.",
                "./.venv/bin/python scripts/run_local_pilot_benchmark.py \\",
                f"  --model {model_id} \\",
                "  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \\",
                f"  --run-id {slug}-local-bfcl-pilot-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    if lane == "prompt-profile-repair":
        return "\n".join(
            [
                "source scripts/env.sh",
                "# Do not redownload; rerun strict local pilots only after a prompt/profile normalizer change.",
                "./.venv/bin/python scripts/run_local_pilot_benchmark.py \\",
                f"  --model {model_id} \\",
                "  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \\",
                f"  --run-id {slug}-strict-profile-repair-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    if lane == "cloud-teacher-proof":
        return "\n".join(
            [
                "source scripts/env.sh",
                "./.venv/bin/python scripts/cloud_backend_preflight.py",
                "# If capacity/auth passes, dispatch a bounded teacher smoke on cloud/Colab/Azure.",
                "./.venv/bin/python scripts/colab_dispatch.py --dry-run",
            ]
        )
    if lane == "specialist-runtime-proof":
        return "\n".join(
            [
                "source scripts/env.sh",
                "./.venv/bin/python scripts/check_specialist_runtime_preflight.py",
                "# Follow with the runtime-specific smoke from the candidate's track plan.",
            ]
        )
    return "\n".join(
        [
            "source scripts/env.sh",
            "./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py",
        ]
    )


def priority_for(item: dict[str, Any], lane: str, coverage_state: str, blocked_reason: str) -> tuple[int, int, str]:
    size_order, _ = parameter_size_bucket(str(item.get("parameters", "")))
    lane_order = {
        "mac-runtime-proof": 0,
        "prompt-profile-repair": 1,
        "evidence-hardening": 2,
        "support-model-proof": 3,
        "cloud-teacher-proof": 4,
        "specialist-runtime-proof": 5,
        "watchlist": 8,
        "deferred": 9,
    }.get(lane, 9)
    state_penalty = 0 if coverage_state in {"blocked", "needs-benchmark", "needs-benchmark-or-proof"} else 1
    reason_penalty = 1 if "open local weights" in blocked_reason else 0
    return lane_order + state_penalty + reason_penalty, size_order, str(item.get("id", ""))


def build_queue(candidates: list[dict[str, Any]], coverage_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    coverage_by_id = {str(row.get("id")): row for row in coverage_rows if row.get("project") == "hermes"}
    rows: list[dict[str, Any]] = []
    for item in candidates:
        candidate_id = str(item.get("id", ""))
        coverage = coverage_by_id.get(candidate_id, {})
        coverage_state = str(coverage.get("coverage_state", "needs-benchmark-or-proof"))
        blocked_reason = str(coverage.get("blocked_reason", ""))
        lane = lane_for(item, coverage_state, blocked_reason)
        _, size_bucket = parameter_size_bucket(str(item.get("parameters", "")))
        row = {
            "id": candidate_id,
            "family": item.get("family", ""),
            "role": item.get("role", ""),
            "environment": item.get("environment", ""),
            "parameters": item.get("parameters", ""),
            "size_bucket": size_bucket,
            "feasibility": item.get("feasibility", ""),
            "coverage_state": coverage_state,
            "blocked_reason": blocked_reason,
            "lane": lane,
            "first_runtime": item.get("first_runtime", ""),
            "next_command": next_command(item, lane),
            "notes": item.get("notes", ""),
        }
        rows.append(row)
    rows.sort(key=lambda row: priority_for(row, str(row["lane"]), str(row["coverage_state"]), str(row["blocked_reason"])))
    return rows


def render_markdown(rows: list[dict[str, Any]], run_id: str) -> str:
    immediate = [
        row
        for row in rows
        if row["lane"] in {"mac-runtime-proof", "prompt-profile-repair", "evidence-hardening", "support-model-proof"}
    ][:25]
    lines = [
        "# Runtime Proof Action Queue",
        "",
        f"Run ID: `{run_id}`",
        f"Created: `{datetime.now(UTC).isoformat()}`",
        "",
        "Purpose: convert the broad Hermes candidate radar into an executable queue. This file does not promote models; it identifies the next proof needed before spending local SSD space, Colab quota, or Azure hours.",
        "",
        "## Immediate Local Queue",
        "",
        "| Priority | Candidate | Lane | Params | Environment | Coverage | Next proof |",
        "|---:|---|---|---|---|---|---|",
    ]
    for index, row in enumerate(immediate, 1):
        next_proof = row["blocked_reason"] or row["first_runtime"] or "run role-specific proof"
        lines.append(
            f"| {index} | `{row['id']}` | `{row['lane']}` | {row['parameters']} | `{row['environment']}` | `{row['coverage_state']}` | {next_proof} |"
        )
    lines.extend(["", "## Lane Counts", "", "| Lane | Count |", "|---|---:|"])
    counts: dict[str, int] = {}
    for row in rows:
        counts[str(row["lane"])] = counts.get(str(row["lane"]), 0) + 1
    for lane, count in sorted(counts.items()):
        lines.append(f"| `{lane}` | {count} |")
    lines.extend(["", "## Command Templates", ""])
    for row in immediate[:12]:
        lines.extend(
            [
                f"### {row['id']}",
                "",
                f"- Lane: `{row['lane']}`",
                f"- Coverage: `{row['coverage_state']}`",
                f"- Blocker: {row['blocked_reason'] or 'none recorded'}",
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
            "- Run local Mac proofs before cloud proofs when the artifact is small enough and a supported runtime exists.",
            "- Use cloud only for teacher/frontier candidates or when local runtime proof is structurally unavailable.",
            "- Route embedders, rerankers, ASR/TTS, and VLM helpers through role-specific support-model proofs rather than Hermes BFCL chat pilots.",
            "- Do not promote from smoke evidence. Promotion still requires strict tool-call, local pilot, selected official benchmark, latency, and rollback evidence.",
            "- Keep model downloads, caches, evals, and exports on `/Volumes/PortableSSD` through `scripts/env.sh`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=ROOT / "MODEL_CANDIDATES.yaml")
    parser.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    parser.add_argument("--output-stem", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    candidates = load_yaml(args.candidates).get("candidates", [])
    coverage_rows = load_json(args.coverage).get("rows", [])
    if not isinstance(candidates, list) or not isinstance(coverage_rows, list):
        raise ValueError("candidate and coverage inputs must contain list rows")
    rows = build_queue([item for item in candidates if isinstance(item, dict)], coverage_rows)
    run_id = args.output_stem.name
    payload = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "source_candidates": str(args.candidates),
        "source_coverage": str(args.coverage),
        "rows": rows,
    }
    args.output_stem.parent.mkdir(parents=True, exist_ok=True)
    json_path = args.output_stem.with_suffix(".json")
    md_path = args.output_stem.with_suffix(".md")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(rows, run_id), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path), "rows": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
