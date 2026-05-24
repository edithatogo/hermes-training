# Project Layout

This repository is the coordination hub for local model work on `/Volumes/PortableSSD`.

## Lanes

| Lane | Path | Purpose | Promotion target |
|---|---|---|---|
| Hermes chat/tool models | `gemma4/`, `lfm2/`, `MODEL_CANDIDATES.yaml` | Fine-tune, benchmark, and package assistant/tool-call models for Hermes Agent. | Hermes can use the model through MLX, Ollama, LM Studio, llama.cpp, or another recorded endpoint. |
| mem0 memory models | `mem0/` | Improve local mem0 extraction, search, recency handling, and cross-agent memory behavior. | mem0 add/search passes benchmark gates and remains rollback-safe. |
| Embeddings/retrieval | `mem0/embeddings/`, `RETRIEVAL_MEMORY.md` | Iterate embedding, reranking, and retriever models for mem0 and Hermes memory/RAG. | Candidate beats `nomic-embed-text:latest` on recall/ranking and latency. |
| Runtime packaging | `ollama-pack/`, `RUNTIME_TARGETS.md`, `mem0/RUNTIME_TARGETS.md` | Convert, serve, and smoke-test models across Ollama, llama.cpp, LM Studio, MLX, and specialist runtimes. | Runtime card records exact commands, endpoint, result, and limitations. |
| Benchmarks | `benchmarks/`, `scripts/run_*benchmark*.py`, `reports/benchmark/` | Keep quality gates reproducible and separated by model role. | Raw outputs and summary reports under `$HERMES_EVAL_ROOT` and `reports/benchmark/`. |

## Artifact Policy

Keep Git for source, configs, benchmark fixtures, cards, and reports. Keep large weights, adapters, GGUFs, indexes, caches, and raw benchmark outputs on SSD-backed artifact roots:

| Artifact type | Default root |
|---|---|
| model caches | `/Volumes/PortableSSD/huggingface` |
| eval outputs | `/Volumes/PortableSSD/hermes-evals` |
| exports / GGUFs | `/Volumes/PortableSSD/hermes-exports` |
| Ollama models | `/Volumes/PortableSSD/Ollama/models` |

## Current Baselines

| Area | Baseline | Status |
|---|---|---|
| Hermes local runtime | `hermes3:8b` and `sam860/LFM2:2.6b` in Ollama | Installed endpoint baseline. |
| Hermes fine-tune lane | Qwen3 4B MLX LoRA experiments | Useful local proof; strict tool-call publication still blocked. |
| mem0 embedder | `nomic-embed-text:latest` through Ollama | Functional baseline; recency-conflict ranking failed first mem0 benchmark. |
| mem0 extractor | `sam860/LFM2:2.6b` through Ollama | Functional baseline; extraction quality needs its own benchmark expansion. |
| Runtime fallback | MLX server, llama.cpp Metal/GGUF, LM Studio | Use run cards before promotion. |

## Development Rule

Do not promote a model because it is new or large. Promote only after the lane-specific benchmark and runtime gates pass.

