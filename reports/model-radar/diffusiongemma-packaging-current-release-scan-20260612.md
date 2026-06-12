# Current Release Scan

Date: 2026-06-12

## Summary

This refresh adds the fresh DiffusionGemma packaging variants surfaced in the
live search.

The live scan found:

- `nvidia/diffusiongemma-26B-A4B-it-NVFP4`
- `mlx-community/diffusiongemma-26B-A4B-it-mxfp4`

The scan keeps the base `google/diffusiongemma-26B-A4B-it` lane in the
research/runtime bucket and does not change the Qwen3.7 guardrail.

## Relevant Findings

| Candidate | Evidence | Track Treatment |
|---|---|---|
| `nvidia/diffusiongemma-26B-A4B-it-NVFP4` | Current Hugging Face search showed the NVFP4 packaging published today. | Diffusion/research lane, not a Hermes adapter target. |
| `mlx-community/diffusiongemma-26B-A4B-it-mxfp4` | Current Hugging Face search showed the MLX packaging published yesterday. | Local runtime comparison point only. |

## Guardrails

- No runtime proof is claimed for the new candidates.
- DiffusionGemma stays in a research/runtime lane only.
- Qwen3.7 remains watchlist-only until official open weights appear.
