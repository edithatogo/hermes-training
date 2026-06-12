# Hybrid Attention and Quantized Packaging Current Release Scan

Date: 2026-06-12

This follow-up scan extends the frontier radar with a long-context hybrid
attention model and a couple of packaging variants that are relevant for
comparison. It does not claim runtime proof or training readiness.

## What Changed

- `openbmb/MiniCPM-SALA` is now tracked as a sparse/linear-attention
  long-context research lane.
- `nvidia/Gemma-4-31B-IT-NVFP4` is now tracked as a quantized packaging
  comparison point for Gemma 4 31B-it.
- `deepseek-ai/DeepSeek-V4-Flash-Base` is now tracked as the base packaging
  reference for the DeepSeek V4 Flash line.

## Radar Summary

| Model | Status | Recommended lane |
|---|---|---|
| `openbmb/MiniCPM-SALA` | Verified official open-weight repo | Research/runtime lane for context-heavy helper workflows |
| `nvidia/Gemma-4-31B-IT-NVFP4` | Verified NVIDIA packaging repo | Cloud packaging comparison only |
| `deepseek-ai/DeepSeek-V4-Flash-Base` | Verified official base repo | Cloud packaging/reference only |

## Guardrails

- Keep `Qwen3.7` watchlist-only until official open weights appear.
- Do not treat these models as default local fine-tune targets.
- Keep the existing Qwen3.6, Hermes 4.3, Gemma 4 12B/31B, MiniCPM5, and
  BitNet lanes as the current local comparison set.

## Sources

- OpenBMB MiniCPM-SALA model card
- NVIDIA Gemma 4 31B IT NVFP4 model card
- DeepSeek-V4-Flash-Base model card
