# EmbeddingGemma Retrieval Refresh - 2026-06-12

## Summary

This follow-up scan captures the official EmbeddingGemma retrieval model and
the packaging lanes that make it useful for Hermes memory and RAG workflows.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| Google | `google/embeddinggemma-300m` | Official 300M embedding baseline for retrieval, clustering, and semantic similarity. |
| Google | `litert-community/embeddinggemma-300m` | Official LiteRT packaging lane for edge/helper deployment. |
| Google | `mlx-community/embeddinggemma-300m-4bit` | Fresh Mac-local MLX packaging for Hermes memory/RAG experiments. |
| Google | `lmstudio-community/embeddinggemma-300m-qat-GGUF` | GGUF packaging lane for local runtime comparison. |

## Watchlist Status

- Keep the lane separated from chat-generation candidates.
- Runtime proof and retrieval evaluation remain separate gates.

## Decision

- Add the new EmbeddingGemma repos to `MODEL_CANDIDATES.yaml`.
- Update the radar docs to keep the lane in the retrieval bucket.
