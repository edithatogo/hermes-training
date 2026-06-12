# Specification: EmbeddingGemma Retrieval Refresh

## Overview

Capture the official `google/embeddinggemma-300m` retrieval model and the
newest LiteRT, MLX, and GGUF packaging lanes that make it useful for Hermes
memory and RAG workflows.

## Scope

- Add `google/embeddinggemma-300m`.
- Add `litert-community/embeddinggemma-300m`.
- Add `mlx-community/embeddinggemma-300m-4bit`.
- Add `lmstudio-community/embeddinggemma-300m-qat-GGUF`.
- Keep the lane clearly separated from chat-generation models.

## Out Of Scope

- No new runtime proof in this slice.
- No fine-tuning or benchmark claim.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new EmbeddingGemma entries.
- The release scan notes mention the new retrieval lane.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the official model card and the packaging lanes are source-backed
  and directly relevant to Hermes memory/RAG.
- Remaining gap: runtime proof and retrieval evaluation remain separate gates.
