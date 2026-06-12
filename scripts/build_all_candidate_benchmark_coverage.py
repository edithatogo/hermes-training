#!/usr/bin/env python3
"""Build a benchmark coverage matrix for every Hermes and mem0 candidate."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
DEFAULT_RUN_ID = "all-candidate-benchmark-coverage-20260612"
DEFAULT_OUT = ROOT / "reports" / "benchmark" / "coverage"


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML object")
    return data


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def report_index() -> list[Path]:
    return sorted(path for path in REPORTS.rglob("*") if path.is_file() and path.suffix in {".md", ".json", ".txt"})


def evidence_paths(candidate_id: str, notes: str, reports: list[Path]) -> list[str]:
    paths: set[str] = set()
    for match in re.findall(r"`([^`]*(?:reports|/Volumes/PortableSSD/hermes-evals)[^`]*)`", notes):
        if match.startswith("reports/"):
            paths.add(match)
    aliases = {
        "google/gemma-4-E2B-it-qat-q4_0-gguf": ["gemma4-e2b-q4", "gemma4-e2b-it-packaging", "gemma-4-E2B_q4_0"],
        "LGAI-EXAONE/EXAONE-4.0-1.2B": ["exaone4-12b", "EXAONE-4.0-1.2B-GGUF"],
        "LiquidAI/LFM2.5-1.2B-Instruct": ["lfm25-1.2b-instruct", "LFM2.5-1.2B-Instruct"],
        "LiquidAI/LFM2.5-1.2B-Thinking": ["lfm25-1.2b-thinking", "LFM2.5-1.2B-Thinking"],
        "LiquidAI/LFM2.5-8B-A1B-GGUF": ["lfm25-8b-a1b", "LFM2.5-8B-A1B"],
        "microsoft/bitnet-b1.58-2B-4T": ["bitnet-b158-2b", "BitNet-b1.58-2B-4T"],
        "CohereLabs/North-Mini-Code-1.0": ["north-mini-code", "North-Mini-Code-1.0"],
        "unsloth/North-Mini-Code-1.0-GGUF": ["north-mini-code", "North-Mini-Code-1.0", "north-mini-code-gguf"],
        "mlx-community/gemma-4-e2b-it-4bit": ["gemma4-e2b-mlx", "gemma-4-e2b-it-4bit"],
        "Qwen/Qwen3-Embedding-0.6B": ["qwen3-embedding-0.6b", "qwen3-06b-embedding"],
        "Qwen/Qwen3-Reranker-0.6B": ["qwen3-0-6b", "qwen3-06b", "Qwen3-Reranker-0.6B"],
    }
    needles = {candidate_id, normalize(candidate_id), *aliases.get(candidate_id, [])}
    leaf = candidate_id.split("/")[-1].replace(":", "-")
    needles.add(leaf)
    needles.add(normalize(leaf))
    for path in reports:
        rel_path = rel(path)
        rel_norm = normalize(rel_path)
        if any(needle and (needle in rel_path or normalize(needle) in rel_norm) for needle in needles):
            paths.add(rel_path)
    return sorted(paths)


def hermes_benchmark_kind(item: dict[str, Any]) -> str:
    role = str(item.get("role", ""))
    env = str(item.get("environment", ""))
    family = str(item.get("family", ""))
    if role == "retrieval" or env == "retrieval":
        return "mem0 retrieval / embedding-reranking benchmark"
    if "multimodal" in str(item.get("tier", "")) or any(token in family for token in ["asr", "tts", "diffusion"]):
        return "support-lane modality benchmark"
    if role in {"local-finetune", "local-runtime"}:
        return "Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval"
    if role in {"cloud-teacher", "hosted-teacher", "cloud-finetune"}:
        return "cloud teacher/runtime smoke plus Hermes strict tool-call sample"
    if role == "research-runtime":
        return "specialist runtime proof"
    if role == "watchlist":
        return "watchlist only"
    return "runtime smoke plus role-specific benchmark"


def mem0_benchmark_kind(item: dict[str, Any]) -> str:
    role = str(item.get("role", ""))
    if role == "embedder":
        return "embedding retrieval suite plus collection migration proof"
    if role == "reranker":
        return "fixed reranking suite, expanded replay, live multi-result fixture"
    if role == "retriever":
        return "late-interaction retriever suite plus separate index proof"
    if role == "extractor":
        return "memory extraction JSON/durability suite"
    return "mem0 role-specific benchmark"


def blocked_reason(item: dict[str, Any], notes: str, project: str) -> str:
    text = notes.lower()
    feasibility = str(item.get("feasibility", ""))
    status = str(item.get("status", ""))
    role = str(item.get("role", ""))
    env = str(item.get("environment", ""))
    params = str(item.get("parameters", "")).lower()

    has_positive_evidence = any(token in text for token in ["passed", "reached", "completed", "runtime-proven", "smoke passed"])

    if status == "access-gated":
        return "blocked on gated/authenticated model access"
    if status == "runtime-blocked":
        return "blocked by current local runtime support"
    if ("403" in text or feasibility == "needs-auth") and not has_positive_evidence:
        return "blocked on gated/authenticated model access"
    if "no verified public" in text or feasibility in {"speculative", "hosted-preview-only"} or role == "watchlist":
        return "blocked because open local weights or a supported public runtime are not verified"
    normalized_text = normalize(text)
    if (
        "unsupported" in text
        or "missing-cohere2moe" in normalized_text
        or "unknown-model-architecture-cohere2moe" in normalized_text
        or "parameters-not-in-model" in normalized_text
    ):
        return "blocked by current local runtime support"
    if ("timed out" in text or "stalled" in text) and not has_positive_evidence:
        return "blocked by local timeout/stall; needs cloud/offload or narrower harness"
    if "empty" in text or "no assistant content" in text:
        return "blocked by empty/no-content generation under the strict prompt"
    if "strict" in text and ("0.000" in text or "failed" in text or "formatting" in text):
        return "blocked by strict Hermes tool-call formatting failure"
    if (status == "runtime-proof-needed" or feasibility == "needs-runtime-proof") and not has_positive_evidence:
        return "blocked until runtime artifact/load proof exists"
    if feasibility == "cloud-only" or env == "azure-cuda":
        return "blocked from local Mac benchmark; requires cloud capacity and cost/auth gate"
    if any(size in params for size in ["120b", "235b", "550b", "ultra", "a55b"]):
        return "blocked from local Mac benchmark by model size; cloud teacher lane only"
    if project == "mem0" and status == "candidate":
        return "not blocked permanently; benchmark gate is still missing or incomplete"
    return ""


def quality_state(item: dict[str, Any], evidence: list[str], reason: str, project: str) -> str:
    notes = str(item.get("notes", "")).lower()
    status = str(item.get("status", ""))
    feasibility = str(item.get("feasibility", ""))
    if reason and ("benchmark gate is still missing" not in reason):
        return "blocked"
    if project == "mem0" and status in {
        "working-default",
        "working-default-clean-root-smoked",
        "benchmarked-cpu-mps-not-promoted",
        "source-model-benchmarked",
        "isolated-fixture-proven",
        "live-read-wrapper-smoked",
        "installed-baseline",
    }:
        return "benchmarked-not-necessarily-promoted"
    if project == "hermes" and evidence and any(token in notes for token in ["runtime-proven", "passed", "completed", "scored", "smoke", "reached"]):
        if any(token in notes for token in ["strict held-out score was `0.250`", "strict hermes tool-call pass was `0.000`", "0.000", "0/3"]):
            return "benchmarked-not-promoted"
        if any(token in notes for token in ["not promoted", "not a default replacement", "quality ceiling", "benchmark-failing"]):
            return "benchmarked-not-promoted"
        return "smoke-or-pilot-only"
    if any(token in notes for token in ["passed", "reached", "completed", "scored", "smoke passed"]):
        if any(token in notes for token in ["not promotion", "not promoted", "do not promote", "keep as candidate", "candidate evidence"]):
            return "benchmarked-not-promoted"
        return "smoke-or-pilot-only"
    if "1.000" in notes and evidence:
        return "benchmarked"
    if evidence and any(token in notes for token in ["smoke", "pilot", "proof"]):
        return "smoke-or-pilot-only"
    if evidence:
        return "evidence-present-needs-review"
    if feasibility == "ready":
        return "needs-benchmark"
    return "needs-benchmark-or-proof"


def benchmark_appropriateness(state: str, benchmark_kind: str, evidence: list[str], notes: str) -> str:
    text = notes.lower()
    if state == "blocked":
        return "not benchmarkable until blocker is cleared"
    if "smoke" in text or "pilot" in text or len(evidence) <= 1:
        return "smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion"
    if "embedding" in benchmark_kind or "reranking" in benchmark_kind or "retriever" in benchmark_kind:
        return "requires expanded/adversarial retrieval replay before default promotion"
    if "strict tool-call" in benchmark_kind:
        return "strict tool-call gate is appropriate for Hermes promotion; pilot ties must be broken with official/expanded suites"
    return "role-appropriate benchmark still needs promotion-grade coverage review"


def build_rows(project: str, candidates: list[dict[str, Any]], reports: list[Path]) -> list[dict[str, Any]]:
    rows = []
    for item in candidates:
        notes = str(item.get("notes", ""))
        evidence = evidence_paths(str(item.get("id", "")), notes, reports)
        kind = hermes_benchmark_kind(item) if project == "hermes" else mem0_benchmark_kind(item)
        reason = blocked_reason(item, notes, project)
        state = quality_state(item, evidence, reason, project)
        rows.append(
            {
                "project": project,
                "id": item.get("id"),
                "role": item.get("role"),
                "family": item.get("family"),
                "environment_or_runtime": item.get("environment") or item.get("runtime"),
                "feasibility_or_status": item.get("feasibility") or item.get("status"),
                "benchmark_kind": kind,
                "coverage_state": state,
                "blocked_reason": reason,
                "benchmark_appropriateness": benchmark_appropriateness(state, kind, evidence, notes),
                "evidence": evidence,
            }
        )
    return rows


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# All-Candidate Benchmark Coverage - 2026-06-12",
        "",
        f"Run ID: `{summary['run_id']}`",
        f"Created: `{summary['created_at']}`",
        "",
        "## Direct Answer",
        "",
        "No: the repo has benchmark evidence for the active Hermes and mem0 lanes, but not promotion-grade benchmark coverage for every candidate in the registries.",
        "",
        "The three-case smokes are appropriate only as liveness and regression checks. They are not sufficiently discriminating when multiple candidates tie. Promotion requires the role-specific expanded suites recorded below.",
        "",
        "## Runtime-Proof Queue",
        "",
        "The executable follow-up queue is generated at [`runtime-proof-action-queue-20260613.md`](./runtime-proof-action-queue-20260613.md). It separates Mac runtime proofs, prompt-profile repairs, support-model proofs, cloud teacher proofs, specialist runtime proofs, and watchlist entries so the remaining blocked Hermes candidates can be worked in bounded batches.",
        "",
        "## Counts",
        "",
        "| Project | Coverage state | Count |",
        "|---|---|---:|",
    ]
    for project, states in summary["counts"].items():
        for state, count in sorted(states.items()):
            lines.append(f"| {project} | `{state}` | {count} |")
    lines.extend(
        [
            "",
            "## Benchmark Policy",
            "",
            "| Lane | Minimum useful gate | Promotion-grade gate |",
            "|---|---|---|",
            "| Hermes chat/tool-call | runtime smoke plus held-out strict tool-call | held-out strict, mirrored strict, local pilots, selected official/lm-eval coverage, and failure analysis |",
            "| Hermes teacher/frontier | runtime proof plus strict tool-call sample | cloud/local repeatable endpoint, strict tool-call comparison, teacher-eval usefulness, cost/capacity record |",
            "| mem0 embedder | direct retrieval smoke | expanded/adversarial retrieval, collection migration proof, rollback proof, latency and memory footprint |",
            "| mem0 reranker | fixed rerank smoke | expanded replay, live multi-result fixture, cold/warm latency, vector fallback |",
            "| mem0 retriever | service/index smoke | separate index lifecycle, expanded replay, rollback/default isolation proof |",
            "| mem0 extractor | JSON extraction smoke | expanded durable extraction, forbidden-hit and empty-case gates, latency |",
            "",
            "## Blocked Reasons",
            "",
            "| Project | Candidate | State | Blocked reason | Evidence |",
            "|---|---|---|---|---|",
        ]
    )
    for row in summary["rows"]:
        if row["coverage_state"] == "blocked":
            evidence = "<br>".join(f"`{path}`" for path in row["evidence"][:3])
            lines.append(
                f"| {row['project']} | `{row['id']}` | `{row['coverage_state']}` | {row['blocked_reason']} | {evidence} |"
            )
    lines.extend(
        [
            "",
            "## Every Candidate",
            "",
            "| Project | Candidate | Role | Status | Benchmark kind | Coverage | Appropriateness / next gate |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in summary["rows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["project"],
                    f"`{row['id']}`",
                    str(row.get("role") or ""),
                    f"`{row.get('feasibility_or_status') or ''}`",
                    row["benchmark_kind"],
                    f"`{row['coverage_state']}`",
                    row["blocked_reason"] or row["benchmark_appropriateness"],
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    reports = report_index()
    hermes = load_yaml(ROOT / "MODEL_CANDIDATES.yaml").get("candidates", [])
    mem0 = load_yaml(ROOT / "mem0" / "MODEL_CANDIDATES.yaml").get("candidates", [])
    if not isinstance(hermes, list) or not isinstance(mem0, list):
        raise ValueError("candidate registries must contain list-valued candidates")

    rows = build_rows("hermes", hermes, reports) + build_rows("mem0", mem0, reports)
    counts: dict[str, dict[str, int]] = {}
    for project in {"hermes", "mem0"}:
        counter = Counter(row["coverage_state"] for row in rows if row["project"] == project)
        counts[project] = dict(counter)
    summary = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "candidate_count": len(rows),
        "counts": counts,
        "rows": rows,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / f"{args.run_id}.json"
    md_path = args.output_dir / f"{args.run_id}.md"
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path), "counts": counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
