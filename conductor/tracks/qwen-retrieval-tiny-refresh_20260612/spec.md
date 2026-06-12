# Specification: Qwen Retrieval Tiny Refresh

## Overview

Hermes memory and retrieval need a small official Qwen lane that is easier to
fit on a 32GB Mac than the 4B retrieval pair.

This refresh focuses on:

- `Qwen/Qwen3-Embedding-0.6B`
- `Qwen/Qwen3-Reranker-0.6B`

## Scope

- Verify the current published status of the official small Qwen retrieval
  models.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, and `HANDOFF.md`.
- Record a concise scan report of why the 0.6B pair is the better memory/RAG
  fit for the Mac lane.

## Out Of Scope

- No chat SFT claims.
- No local training runs.
- No promotion beyond retrieval/runtime proof.

## Acceptance Criteria

- The radar includes the official Qwen 0.6B embedding and reranker models.
- The docs keep the models in retrieval/helper lanes.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the lane is source-backed and already aligned with the mem0 work.
- Remaining gap: separate runtime proof for the embedding model if needed.
