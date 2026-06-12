# Qwen3-VL Multimodal Retrieval Refresh - 2026-06-12

## Summary

This follow-up scan captures the official Qwen3-VL multimodal retrieval
models and the packaging lanes that make them usable for Hermes screenshot,
document-image, and video retrieval workflows.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| Qwen | `Qwen/Qwen3-VL-Embedding-2B` | Official compact multimodal retrieval embedder for text, images, screenshots, and video. |
| Qwen | `Qwen/Qwen3-VL-Embedding-8B` | Official higher-capacity multimodal retrieval embedder. |
| Qwen | `Qwen/Qwen3-VL-Reranker-8B` | Official multimodal reranker to pair with the embedding lane. |
| Qwen | `mlx-community/Qwen3-VL-Embedding-2B-8bit` | Fresh Mac-local MLX packaging for the smaller embedder. |
| Qwen | `aiteza/Qwen3-VL-Embedding-8B-GGUF` | GGUF packaging lane for local runtime comparison. |
| Qwen | `mradermacher/Qwen3-VL-Reranker-8B-GGUF` | GGUF packaging lane for the multimodal reranker. |
| Qwen | `Zeknes/Qwen3-VL-Reranker-8B-MLX-4bit` | Fresh Mac-local MLX packaging lane for the reranker. |

## Watchlist Status

- Keep the lane separated from chat-generation candidates.
- Runtime proof and retrieval evaluation remain separate gates.

## Decision

- Add the new Qwen3-VL retrieval repos to `MODEL_CANDIDATES.yaml`.
- Update the radar docs so the multimodal retrieval lane is tracked distinctly
  from the text-only embedding and reranking candidates.
