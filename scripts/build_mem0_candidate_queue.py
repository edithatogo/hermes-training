#!/usr/bin/env python3
"""Build a markdown execution queue from mem0/MODEL_CANDIDATES.yaml."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


ROLE_ORDER = {
    "reranker": 0,
    "embedder": 1,
    "extractor": 2,
    "retriever": 3,
    "summarizer": 4,
    "store": 5,
}

STATUS_ORDER = {
    "working-default": 0,
    "working-default-clean-root-smoked": 0,
    "live-read-wrapper-smoked": 1,
    "isolated-fixture-proven": 1,
    "benchmarked-cpu-mps-not-promoted": 2,
    "fixed-suite-benchmarked": 2,
    "source-model-benchmarked": 2,
    "installed-baseline": 3,
    "candidate-runtime-id-verified": 4,
    "candidate": 4,
    "runtime-proof-needed": 3,
    "planned": 5,
    "rejected": 9,
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML object")
    return data


def first_runtime(candidate: dict[str, Any]) -> str:
    runtime = candidate.get("runtime", [])
    if isinstance(runtime, list) and runtime:
        return str(runtime[0])
    return str(runtime or "")


def queue_priority(candidate: dict[str, Any]) -> tuple[int, int, str]:
    return (
        STATUS_ORDER.get(str(candidate.get("status")), 8),
        ROLE_ORDER.get(str(candidate.get("role")), 8),
        str(candidate.get("id", "")),
    )


def command_for(candidate: dict[str, Any]) -> str:
    model_id = str(candidate.get("id", "<model>"))
    role = str(candidate.get("role", ""))
    runtime = first_runtime(candidate)
    status = str(candidate.get("status", ""))
    slug = (
        model_id.replace("/", "-")
        .replace(":", "-")
        .replace(".", "-")
        .replace("_", "-")
        .lower()
    )

    if role == "embedder" and runtime == "ollama":
        return "\n".join(
            [
                "./.venv/bin/python scripts/run_ollama_embedding_benchmark.py \\",
                f"  --model {model_id} \\",
                "  --suite benchmarks/embeddings/memory_retrieval_suite.json \\",
                f"  --run-id embedding-{slug}-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    if role == "embedder" and runtime in {"sentence-transformers", "transformers"}:
        return "\n".join(
            [
                "./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \\",
                f"  --model {model_id} \\",
                "  --device mps \\",
                "  --suite benchmarks/embeddings/memory_retrieval_suite.json \\",
                f"  --run-id embedding-{slug}-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    if role == "reranker" and runtime == "local-python":
        strategy = (
            "score_plus_created_at_rank_close_margin"
            if status == "live-read-wrapper-smoked"
            else "score_plus_created_at_rank"
        )
        return "\n".join(
            [
                "./.venv/bin/python scripts/mem0_rerank_search.py \\",
                '  "What is the active mem0 Qdrant collection?" \\',
                "  --tool cmd \\",
                f"  --strategy {strategy} \\",
                "  --recency-weight 0.20 \\",
                "  --timeout-s 60",
            ]
        )
    if role == "reranker":
        if "bge-reranker-v2-m3-mlx" in model_id:
            if status == "isolated-fixture-proven":
                return "\n".join(
                    [
                        "# Opt-in guarded read mode is available; run bounded cold/warm latency probes before any default integration.",
                        "HF_HUB_DISABLE_XET=1 ./.venv/bin/python scripts/run_mem0_read_latency_probe.py \\",
                        "  --mode mlx-bge \\",
                        '  --query "What is the active mem0 Qdrant collection?" \\',
                        "  --iterations 1 \\",
                        "  --read-wall-timeout-s 60 \\",
                        "  --subprocess-read \\",
                        "  --fallback-to-vector \\",
                        "  --cache-ttl-s 300",
                    ]
                )
            return "\n".join(
                [
                    "# MLX BGE reranker repo ID is verified. Run a bounded Apple Silicon load/scoring proof first.",
                    "./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \\",
                    "  --strategy mlx_cross_encoder \\",
                    f"  --model {model_id} \\",
                    "  --mlx-max-length 1024 \\",
                    "  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \\",
                    f"  --run-id rerank-{slug}-$(date +%Y%m%d-%H%M%S)",
                ]
            )
        if "Qwen3-Reranker" in model_id:
            if model_id == "onnx-community/Qwen3-Reranker-0.6B-ONNX":
                return "\n".join(
                    [
                        "# ONNX candidate is Transformers.js-oriented; this fail-closed bridge proof keeps Node tooling on the SSD.",
                        "./.venv/bin/python scripts/run_qwen3_onnx_transformersjs_smoke.py \\",
                        "  --run-id qwen3-0-6b-onnx-transformersjs-$(date +%Y%m%d-%H%M%S) \\",
                        "  --limit-cases 1 \\",
                        "  --max-length 512 \\",
                        "  --timeout-s 180",
                    ]
                )
            benchmark_model = (
                "Qwen/Qwen3-Reranker-0.6B"
                if model_id == "onnx-community/Qwen3-Reranker-0.6B-ONNX"
                else model_id
            )
            setup_note = (
                "# ONNX candidate is Transformers.js-oriented; this Python smoke uses the source HF model with the same yes/no scoring."
                if benchmark_model != model_id
                else "# First ensure the model is available in the SSD Hugging Face cache."
            )
            return "\n".join(
                [
                    setup_note,
                    "./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \\",
                    "  --strategy qwen3_causal_lm \\",
                    f"  --model {benchmark_model} \\",
                    "  --qwen3-device auto \\",
                    "  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \\",
                    f"  --run-id rerank-{slug}-$(date +%Y%m%d-%H%M%S)",
                ]
            )
        return "\n".join(
            [
                "# First install optional reranker deps if needed.",
                "python -m pip install -r requirements-mem0-rerankers.txt",
                "./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \\",
                "  --strategy cross_encoder \\",
                f"  --model {model_id} \\",
                "  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \\",
                f"  --run-id rerank-{slug}-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    if role == "extractor":
        if status == "runtime-proof-needed" or runtime.endswith("-gguf"):
            return "\n".join(
                [
                    "# First create or load a local runtime artifact for this model.",
                    "# Then expose it through an OpenAI-compatible /v1/chat/completions endpoint.",
                    "# After endpoint proof, run:",
                    "./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \\",
                    "  --model <local-model-id> \\",
                    "  --base-url http://127.0.0.1:<port>/v1 \\",
                    "  --suite benchmarks/mem0_extraction/smoke_suite.json \\",
                    f"  --run-id extraction-{slug}-$(date +%Y%m%d-%H%M%S)",
                ]
            )
        return "\n".join(
            [
                "./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \\",
                f"  --model {model_id} \\",
                "  --base-url http://127.0.0.1:11434/v1 \\",
                "  --suite benchmarks/mem0_extraction/smoke_suite.json \\",
                f"  --run-id extraction-{slug}-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    if role == "retriever":
        return "\n".join(
            [
                "# Build a separate retriever service/index before benchmarking.",
                "# Do not reuse the dense Qdrant collection for late-interaction vectors.",
            ]
        )
    return "# No default command yet."


def blocker_for(candidate: dict[str, Any]) -> str:
    status = str(candidate.get("status", ""))
    role = str(candidate.get("role", ""))
    runtime = first_runtime(candidate)
    dims = candidate.get("embedding_dims")
    if status in {"working-default", "installed-baseline"}:
        return "baseline; keep as rollback and compare only"
    if status == "working-default-clean-root-smoked":
        return "baseline recovered in clean SSD Ollama root; keep as rollback and compare only"
    if status == "live-read-wrapper-smoked":
        return "live read-only wrapper smoke passed; keep read-only until broader coverage"
    if status == "isolated-fixture-proven":
        return "first bounded cache-hit daily-use probe passed; keep opt-in read mode until broader cold/warm latency proof"
    if status == "benchmarked-cpu-mps-not-promoted":
        return "benchmarked but not promoted; keep separate collection or artifact"
    if status == "fixed-suite-benchmarked":
        return "fixed suite passed; run expanded replay and isolated fixture before live integration"
    if status == "source-model-benchmarked":
        if candidate.get("id") == "onnx-community/Qwen3-Reranker-0.6B-ONNX":
            return "source Qwen/Qwen3-Reranker-0.6B passed suites; ONNX package remains blocked pending bounded CPU/CoreML proof"
        return "source HF model passed fixed and expanded suites; ONNX bridge still needs runtime proof"
    if status == "candidate-runtime-id-verified" and role == "reranker" and runtime == "mlx":
        return "model repo verified; MLX load/scoring proof is ready before live mem0 integration"
    if role == "embedder" and runtime in {"sentence-transformers", "transformers"}:
        return "requires model acquisition/load proof and memory-footprint check"
    if role == "embedder" and dims in {"unknown", "variable"}:
        return "verify embedding dimension before creating collection"
    if role == "reranker" and runtime != "local-python":
        return "requires model acquisition/load proof; fixed-candidate harness is ready"
    if role == "retriever":
        return "needs separate index/service shape"
    if status == "runtime-proof-needed":
        return "needs local artifact or endpoint proof"
    return "none recorded"


def render_queue(data: dict[str, Any]) -> str:
    candidates = data.get("candidates", [])
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list")
    ordered = sorted((item for item in candidates if isinstance(item, dict)), key=queue_priority)

    lines = [
        "# mem0 Candidate Execution Queue",
        "",
        f"Target: {data.get('project_target', '')}",
        "",
        "## Current Default",
        "",
        "| Component | Value |",
        "|---|---|",
    ]
    current = data.get("current_default", {})
    if isinstance(current, dict):
        for key in ["vector_store", "collection", "embedder", "embedder_runtime", "embedding_dims", "extractor", "extractor_runtime", "status"]:
            lines.append(f"| {key} | `{current.get(key, '')}` |")
    lines.extend(
        [
            "",
            "## Queue",
            "",
            "| Priority | Candidate | Role | Status | First runtime | First gate | Blocker / note |",
            "|---:|---|---|---|---|---|---|",
        ]
    )
    for index, candidate in enumerate(ordered, 1):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    f"`{candidate.get('id', '')}`",
                    str(candidate.get("role", "")),
                    str(candidate.get("status", "")),
                    first_runtime(candidate),
                    str(candidate.get("first_gate", "")),
                    blocker_for(candidate),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Candidate Commands", ""])
    for candidate in ordered:
        lines.extend(
            [
                f"### {candidate.get('id', '')}",
                "",
                f"- Role: `{candidate.get('role', '')}`",
                f"- Status: `{candidate.get('status', '')}`",
                f"- Blocker: {blocker_for(candidate)}",
                "",
                "```bash",
                "source scripts/env.sh",
                command_for(candidate),
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=Path("mem0/MODEL_CANDIDATES.yaml"))
    parser.add_argument("--output", type=Path, default=Path("reports/model-radar/mem0-candidate-queue.md"))
    args = parser.parse_args()

    markdown = render_queue(load_yaml(args.candidates))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
