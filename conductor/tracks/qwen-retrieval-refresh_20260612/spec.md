# Specification: Qwen Retrieval Refresh

## Overview

Hermes memory and retrieval should track the current official Qwen retrieval
models as separate lanes from chat SFT models.

This refresh focuses on:

- `Qwen/Qwen3-Embedding-4B`
- `Qwen/Qwen3-Reranker-4B`

## Scope

- Verify the current published status of the official Qwen retrieval models.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, and `HANDOFF.md`.
- Record a concise scan report of the retrieval lane and its fit for Hermes
  memory/RAG.

## Out Of Scope

- No chat SFT claims.
- No local training runs.
- No promotion beyond retrieval/runtime proof.

## Acceptance Criteria

- The radar includes the official Qwen embedding and reranker models.
- The docs keep the models in retrieval/helper lanes.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the lane is source-backed and separated from chat model claims.
- Remaining gap: runtime proof is separate from the radar refresh itself.
