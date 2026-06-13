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
    "broader-latency-proven-opt-in": 1,
    "benchmarked-cpu-mps-not-promoted": 2,
    "extraction-benchmarked-not-promoted": 2,
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


def embedding_suite_for(candidate: dict[str, Any]) -> str:
    first_gate = str(candidate.get("first_gate", ""))
    status = str(candidate.get("status", ""))
    if first_gate == "differentiation-suite" or status in {
        "benchmarked-cpu-mps-not-promoted",
        "source-model-benchmarked",
    }:
        return "benchmarks/embeddings/memory_retrieval_differentiation_suite.json"
    return "benchmarks/embeddings/memory_retrieval_suite.json"


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

    if status == "access-gated":
        return "\n".join(
            [
                "# Access-gated candidate. Do not rerun benchmark commands until the account has accepted access and a metadata-only check passes.",
                f"# Candidate: {model_id}",
                "# Use the separately benchmarked open/local package as the comparison lane until access is granted.",
            ]
        )
    if status == "runtime-blocked":
        return "\n".join(
            [
                "# Runtime-blocked candidate. Do not rerun the same benchmark command until the dependency/runtime blocker changes.",
                f"# Candidate: {model_id}",
                "# Recheck the model card and local dependency stack first, then regenerate this queue.",
            ]
        )

    if role == "embedder" and runtime == "ollama":
        suite = embedding_suite_for(candidate)
        return "\n".join(
            [
                "./.venv/bin/python scripts/run_ollama_embedding_benchmark.py \\",
                f"  --model {model_id} \\",
                f"  --suite {suite} \\",
                f"  --run-id embedding-{slug}-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    if role == "embedder" and runtime == "mlx" and "jina-embeddings-v5-omni-small" in model_id:
        task_type = "text-matching" if "text-matching" in model_id else "retrieval"
        suite = embedding_suite_for(candidate)
        return "\n".join(
            [
                "# Jina MLX embeddings are custom-code repos; clone and load them through the dedicated MLX benchmark runner.",
                "./.venv/bin/python scripts/run_jina_mlx_embedding_benchmark.py \\",
                f"  --model {model_id} \\",
                f"  --task-type {task_type} \\",
                f"  --suite {suite} \\",
                f"  --run-id embedding-{slug}-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    if role == "embedder" and runtime == "llama.cpp":
        lines = [
            "# GGUF embedding candidate; prefer batched/server proof before default mem0 promotion.",
            "./.venv/bin/python scripts/run_llama_cpp_embedding_benchmark.py \\",
            f"  --model {model_id} \\",
        ]
        if candidate.get("model_path"):
            lines.append(f"  --model-path {candidate['model_path']} \\")
        else:
            lines.append("  --model-path <path-to-embedding-gguf> \\")
        if candidate.get("llama_embedding_bin"):
            lines.append(f"  --llama-embedding-bin {candidate['llama_embedding_bin']} \\")
        if candidate.get("ctx_size"):
            lines.append(f"  --ctx-size {candidate['ctx_size']} \\")
        if candidate.get("pooling"):
            lines.append(f"  --pooling {candidate['pooling']} \\")
        if candidate.get("embd_normalize") is not None:
            lines.append(f"  --embd-normalize {candidate['embd_normalize']} \\")
        lines.extend(
            [
                "  --suite benchmarks/embeddings/memory_retrieval_differentiation_suite.json \\",
                f"  --run-id embedding-{slug}-$(date +%Y%m%d-%H%M%S)",
            ]
        )
        if model_id == "lmstudio-community/embeddinggemma-300m-qat-GGUF":
            lines.extend(
                [
                    "",
                    "# Opt-in Hermes read path after rendering an EmbeddingGemma mem0 profile:",
                    './.venv/bin/python scripts/mem0_read.py "active collection" \\',
                    "  --mode embeddinggemma-proxy \\",
                    "  --mem0-config-path /Volumes/PortableSSD/hermes-evals/mem0-profiles/embeddinggemma-300m-qat-gguf/config.json \\",
                    "  --cache-ttl-s 0",
                ]
            )
        return "\n".join(lines)
    if role == "embedder" and runtime in {"sentence-transformers", "transformers"}:
        suite = embedding_suite_for(candidate)
        return "\n".join(
            [
                "./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \\",
                f"  --model {model_id} \\",
                "  --device mps \\",
                f"  --suite {suite} \\",
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
            if status in {"isolated-fixture-proven", "broader-latency-proven-opt-in"}:
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
                "./.venv/bin/python -m pip install -r requirements-mem0-rerankers.txt",
                "./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \\",
                "  --strategy cross_encoder \\",
                f"  --model {model_id} \\",
                "  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \\",
                f"  --run-id rerank-{slug}-$(date +%Y%m%d-%H%M%S)",
            ]
        )
    if role == "extractor":
        if model_id == "NousResearch/Hermes-4-14B":
            return "\n".join(
                [
                    "# Hermes 4 Q4 has already failed this gate at 2/7; rerun only after a prompt/template change.",
                    "# First expose the local Hermes 4 GGUF through llama.cpp on http://127.0.0.1:8092/v1.",
                    "./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \\",
                    "  --model hermes-4-14b-q4 \\",
                    "  --base-url http://127.0.0.1:8092/v1 \\",
                    "  --suite benchmarks/mem0_extraction/smoke_suite.json \\",
                    "  --run-id extraction-hermes4-14b-q4-smoke-$(date +%Y%m%d-%H%M%S)",
                ]
            )
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
    model_id = str(candidate.get("id", ""))
    if status in {"working-default", "installed-baseline"}:
        return "baseline; keep as rollback and compare only"
    if status == "working-default-clean-root-smoked":
        return "baseline recovered in clean SSD Ollama root; keep as rollback and compare only"
    if status == "live-read-wrapper-smoked":
        return "live read-only wrapper smoke passed; keep read-only until broader coverage"
    if status == "isolated-fixture-proven":
        return "first bounded cache-hit daily-use probe passed; keep opt-in read mode until broader cold/warm latency proof"
    if status == "broader-latency-proven-opt-in":
        return (
            "broader cold/warm proof passed safely with cold p50 7.404s, "
            "cache-hit p50 4.552s, and rerank p50 0.048s, but remains too slow "
            "for every-turn automatic preludes; keep opt-in read mode"
        )
    if status == "benchmarked-cpu-mps-not-promoted":
        if candidate.get("id") == "BAAI/bge-m3":
            return "expanded 2026-06-13 differentiation suite reached top-1 0.929 / recall@3 1.000, strongest non-GGUF embedder signal; keep separate 1024-dim collection"
        return "benchmarked but not promoted; keep separate collection or artifact"
    if status == "extraction-benchmarked-not-promoted":
        return "extraction benchmark completed but failed promotion gate; keep LFM2 as the default extractor"
    if status == "fixed-suite-benchmarked":
        return "fixed suite passed; run expanded replay and isolated fixture before live integration"
    if status == "source-model-benchmarked":
        if candidate.get("id") == "onnx-community/Qwen3-Reranker-0.6B-ONNX":
            return "source Qwen/Qwen3-Reranker-0.6B passed suites; ONNX package remains blocked pending bounded CPU/CoreML proof"
        if candidate.get("id") == "Qwen/Qwen3-Reranker-4B":
            return "quality proof passed, but CPU latency is too high for default promotion without acceleration or live replay proof"
        if candidate.get("id") == "Qwen/Qwen3-Embedding-4B":
            return "expanded suite passed recall but missed one top-1 recency case; keep behind separate 2560-dim collection and reranking"
        if candidate.get("id") == "jinaai/jina-embeddings-v5-omni-small-mlx":
            return "expanded retrieval suite reached recall 1.000 but top-1 0.833 with two close recency/update misses; prefer text-matching variant for now"
        if candidate.get("id") == "jinaai/jina-embeddings-v5-omni-small-text-matching-mlx":
            return "expanded suite passed at 1.000, but expanded 2026-06-13 differentiation suite reached top-1 0.786 / recall@3 0.929; keep as fast candidate, not default"
        if candidate.get("id") == "lmstudio-community/embeddinggemma-300m-qat-GGUF":
            return (
                "server-backed differentiation and resilient-proxy live mem0 fixture both "
                "reached top-1 1.000 / recall@3 1.000; copied live-store replay reached "
                "recall 1.000 but top-1 match 0.200 and existing no-download rerank "
                "policies did not improve it, so embeddinggemma-proxy stays opt-in"
            )
        if candidate.get("id") == "LiquidAI/LFM2-ColBERT-350M":
            return "expanded retriever benchmark completed; keep opt-in because isolated mem0 fixture trailed close-margin guarded read"
        return "source HF model passed fixed and expanded suites; keep as benchmarked-not-promoted until a role-specific promotion gate passes"
    if status == "candidate-runtime-id-verified" and role == "reranker" and runtime == "mlx":
        return "model repo verified; MLX load/scoring proof is ready before live mem0 integration"
    if candidate.get("id") == "google/embeddinggemma-300m":
        return (
            "Official Google retrieval baseline for mem0 comparison. Gated model with "
            "2048-token context and configurable 128-768 embedding dimensions; direct "
            "smokes on 2026-05-26, 2026-06-12, and 2026-06-13 returned Hugging Face "
            "403 gated-repo errors despite public metadata visibility, so use the "
            "separately benchmarked GGUF package until official access is granted"
        )
    if role == "embedder" and runtime in {"sentence-transformers", "transformers"}:
        return "requires model acquisition/load proof and memory-footprint check"
    if role == "embedder" and runtime == "mlx" and "jina-embeddings-v5-omni-small" in model_id:
        if model_id.endswith("text-matching-mlx"):
            return (
                "2026-06-12 local SSD smoke passed the 3-case mem0 embedding suite at "
                "top-1 1.000 / recall@3 1.000 / MRR 1.000 / nDCG@3 1.000 with "
                "1024-dim embeddings; keep as candidate evidence, not a default "
                "embedder switch"
            )
        return (
            "2026-06-11 retrieval smoke passed at top-1 1.000 / recall@3 1.000 / "
            "MRR 1.000 on the 1-case metadata-database query with 1024-dim "
            "embeddings; verify collection shape before any default switch"
        )
    if role == "embedder" and dims in {"unknown", "variable"}:
        return "verify embedding dimension before creating collection"
    if candidate.get("id") == "Qwen/Qwen3-Embedding-4B":
        return (
            "Potential high-quality local embedder. Runtime and memory footprint must "
            "be proven on the M1 Max before use; the first direct MPS smoke cached "
            "the repo but stalled before producing a benchmark summary, so keep it "
            "queued until a cached or offloaded path is available"
        )
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
