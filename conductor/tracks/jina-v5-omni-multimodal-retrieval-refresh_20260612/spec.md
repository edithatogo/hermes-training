# Specification: Jina V5 Omni Multimodal Retrieval Refresh

## Overview

Capture the official `jinaai/jina-embeddings-v5-omni-small` and
`jinaai/jina-embeddings-v5-omni-nano` models plus the newest MLX and ONNX
packaging lanes that make them useful for Hermes cross-modal retrieval
workflows.

## Scope

- Add `jinaai/jina-embeddings-v5-omni-small`.
- Add `jinaai/jina-embeddings-v5-omni-nano`.
- Add `jinaai/jina-embeddings-v5-omni-small-mlx`.
- Add `jinaai/jina-embeddings-v5-omni-nano-mlx`.
- Add `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx`.
- Add `jinaai/jina-embeddings-v5-omni-nano-retrieval-mlx`.
- Add `onnx-community/jina-embeddings-v5-omni-nano-ONNX`.
- Keep the lane clearly separated from chat-generation models.

## Out Of Scope

- No runtime proof in this slice.
- No fine-tuning or benchmark claim.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new Jina omni entries.
- The release scan notes mention the new multimodal retrieval lane.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the official model cards and the packaging lanes are source-backed
  and directly relevant to Hermes cross-modal retrieval.
- Remaining gap: runtime proof and retrieval evaluation remain separate gates.
