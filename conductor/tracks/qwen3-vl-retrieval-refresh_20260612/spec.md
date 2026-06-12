# Specification: Qwen3-VL Multimodal Retrieval Refresh

## Overview

Capture the official `Qwen/Qwen3-VL-Embedding-2B`, `Qwen/Qwen3-VL-Embedding-8B`,
and `Qwen/Qwen3-VL-Reranker-8B` models plus the newest MLX and GGUF packaging
lanes that make them useful for Hermes multimodal retrieval workflows.

## Scope

- Add `Qwen/Qwen3-VL-Embedding-2B`.
- Add `Qwen/Qwen3-VL-Embedding-8B`.
- Add `Qwen/Qwen3-VL-Reranker-8B`.
- Add `mlx-community/Qwen3-VL-Embedding-2B-8bit`.
- Add `aiteza/Qwen3-VL-Embedding-8B-GGUF`.
- Add `mradermacher/Qwen3-VL-Reranker-8B-GGUF`.
- Add `Zeknes/Qwen3-VL-Reranker-8B-MLX-4bit`.
- Keep the lane clearly separated from chat-generation models.

## Out Of Scope

- No runtime proof in this slice.
- No fine-tuning or benchmark claim.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new Qwen3-VL entries.
- The release scan notes mention the new multimodal retrieval lane.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the official model cards and the packaging lanes are source-backed
  and directly relevant to Hermes multimodal retrieval.
- Remaining gap: runtime proof and retrieval evaluation remain separate gates.
