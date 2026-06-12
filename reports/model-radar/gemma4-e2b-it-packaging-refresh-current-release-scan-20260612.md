# Gemma 4 E2B-it Packaging Refresh - 2026-06-12

## Summary

This follow-up scan captures the official Gemma 4 E2B-it instruction-tuned
repo and the packaging lanes that make it practical for Mac-local helper
workflows.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| Gemma | `google/gemma-4-E2B-it` | Official instruction-tuned E2B lane and the smallest practical Gemma 4 comparison point. |
| Gemma | `litert-community/gemma-4-E2B-it-litert-lm` | LiteRT packaging for the official E2B-it model card. |
| Gemma | `mlx-community/gemma-4-e2b-it-4bit` | Fresh Mac-local MLX packaging point for the E2B-it lane. |

## Watchlist Status

- Keep the E2B q4_0 GGUF runtime proof separate from this packaging refresh.
- Runtime proof remains a separate gate if any of these lanes are used locally.

## Decision

- Add the new Gemma 4 E2B-it repos to `MODEL_CANDIDATES.yaml`.
- Update the radar docs to keep the lane in the edge-runtime bucket.
