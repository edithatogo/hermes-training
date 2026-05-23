# Specification: Model Candidate Evaluation And Selection

## Overview

Define a reproducible evaluation and selection track for Hermes model candidates across local, teacher-baseline, retrieval, and research-runtime lanes. The track is planning-only at setup time: it must create decision structure, evaluation gates, and documentation expectations without browsing for new information, downloading large models, or running candidate benchmarks.

## Goals

- Establish parallel evaluation lanes that can be executed independently without blocking the whole selection process.
- Make Mac-local viability, teacher baseline quality, retrieval utility, research-runtime maturity, and publication readiness comparable through a shared decision record.
- Keep model downloads, benchmark artifacts, and caches bound to SSD-backed roots when future execution work begins.
- Separate candidate evaluation from publication so no model, adapter, or benchmark claim is published without explicit gates and license checks.

## Parallel Evaluation Lanes

### Lane A - Mac-Local Candidates

- Identify small and efficient candidates suitable for MacBook Pro M1 Max, 32GB unified memory, MLX, Ollama, LM Studio, or GGUF runtime proof.
- Define fit checks for memory budget, context length, tool-call behavior, OpenAI-compatible endpoint behavior, and local adapter feasibility.
- Treat local smoke success as runtime proof only until benchmark gates pass.

### Lane B - Hermes 4 And Qwen3.6 Teacher Baselines

- Define teacher/evaluator baseline roles for Hermes 4 and Qwen3.6-family candidates where available.
- Capture expected uses: answer-quality comparison, tool-call repair targets, dataset critique, and benchmark normalization references.
- Require source, version, license, serving endpoint, and cost/runtime notes before any teacher output becomes evidence.

### Lane C - Retrieval And Embedding Candidates

- Evaluate embedding, reranker, and retrieval-memory candidates separately from chat SFT candidates.
- Use retrieval-specific gates such as MTEB-style tasks, document recall, reranking quality, latency, storage footprint, and RAG answer grounding.
- Prevent retrieval wins from being promoted as chat-model wins unless both lanes are explicitly tested.

### Lane D - Subquadratic, Recurrent, And BitNet Research Runtimes

- Track Mamba-family, RWKV/recurrent, KTransformers-style, BitNet, and other research-runtime candidates behind runtime-proof gates.
- Require verified weights, license, reproducible runtime setup, endpoint behavior, and benchmark comparability before promotion.
- Mark unsupported or immature runtimes as research watchlist entries, not product candidates.

### Lane E - Publish / No-Publish Decisions

- Define decision states for each candidate: reject, watchlist, runtime-proof only, benchmark candidate, internal adapter candidate, publish candidate.
- Require license confirmation, benchmark evidence, model card readiness, artifact path review, and explicit user approval before public publication.
- Record why candidates fail gates so future tracks do not repeat the same evaluation work.

## Requirements

- Create a candidate matrix template covering lane, model/runtime, source, license, local feasibility, benchmark plan, storage path, owner notes, decision state, and blockers.
- Define lane-specific scoring dimensions without hard-coding final scores before evidence exists.
- Define promotion gates for moving from watchlist to runtime proof, from runtime proof to benchmark, and from benchmark to publish candidate.
- Define no-publish rules for missing licenses, unsupported runtimes, unnormalized benchmarks, failed tool-call behavior, or artifacts outside SSD-backed roots.
- Reference existing hub doctrine: `requirements.md`, `design.md`, `contracts.md`, `STANDARD_BENCHMARKS.md`, `REPO_MAINTENANCE.md`, and `HANDOFF.md` where applicable.
- Avoid browsing, model downloads, benchmark execution, or large artifact creation during this setup track.

## Acceptance Criteria

- The track contains a `spec.md`, `plan.md`, `metadata.json`, and `index.md`.
- `conductor/tracks.md` contains an unchecked registry entry pointing to this track.
- The plan defines independent work phases for all five lanes and a final synthesis phase.
- The plan includes explicit validation, storage, and publication guardrails.
- No large models, benchmarks, caches, or generated artifacts are downloaded or created by setup.

## Out Of Scope

- Downloading, converting, quantizing, or running large models.
- Executing benchmarks or teacher generations.
- Publishing adapters, model cards, benchmark reports, or Hugging Face artifacts.
- Changing runtime code, benchmark harnesses, or nested model-track repositories.
