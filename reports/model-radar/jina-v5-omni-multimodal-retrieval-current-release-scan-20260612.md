# Jina V5 Omni Multimodal Retrieval Refresh - 2026-06-12

## Summary

This follow-up scan captures the official Jina v5 omni multimodal retrieval
family and the MLX and browser/WebGPU packaging lanes that make it useful for
Hermes cross-modal retrieval workflows.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| Jina | `jinaai/jina-embeddings-v5-omni-small` | Official 2B multimodal embedding baseline for text, image, video, and audio retrieval. |
| Jina | `jinaai/jina-embeddings-v5-omni-nano` | Smaller official multimodal embedding baseline for constrained retrieval workflows. |
| Jina | `jinaai/jina-embeddings-v5-omni-small-mlx` | MLX-native Apple Silicon lane for the small omni model. |
| Jina | `jinaai/jina-embeddings-v5-omni-nano-mlx` | MLX-native Apple Silicon lane for the nano omni model. |
| Jina | `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | Task-specific MLX packaging for text matching. |
| Jina | `jinaai/jina-embeddings-v5-omni-nano-retrieval-mlx` | Task-specific MLX packaging for retrieval. |
| Jina | `onnx-community/jina-embeddings-v5-omni-nano-ONNX` | Browser/WebGPU lane for lightweight client-side retrieval. |

## Watchlist Status

- Keep the lane separated from chat-generation candidates.
- Runtime proof and retrieval evaluation remain separate gates.

## Decision

- Add the new Jina omni retrieval repos to `MODEL_CANDIDATES.yaml`.
- Update the radar docs so the multimodal retrieval lane is tracked distinctly
  from the text-only embedding and reranking candidates.
