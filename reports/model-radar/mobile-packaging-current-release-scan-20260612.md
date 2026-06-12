# Current Release Scan

Date: 2026-06-12

## Summary

This refresh adds the fresh mobile and lightweight packaging variants surfaced
in live search.

The live scan found:

- `google/gemma-4-E2B-it-qat-mobile-transformers`
- `google/gemma-4-E4B-it-qat-mobile-transformers`
- `openbmb/MiniCPM-V-4.6-BNB`

The scan keeps the base Gemma 4 and MiniCPM-V 4.6 lanes in the
research/runtime buckets and does not change the Qwen3.7 guardrail.

## Relevant Findings

| Candidate | Evidence | Track Treatment |
|---|---|---|
| `google/gemma-4-E2B-it-qat-mobile-transformers` | Current Hugging Face search showed the QAT Mobile package. | Lightweight runtime comparison point only. |
| `google/gemma-4-E4B-it-qat-mobile-transformers` | Current Hugging Face search showed the QAT Mobile package. | Lightweight runtime comparison point only. |
| `openbmb/MiniCPM-V-4.6-BNB` | Current Hugging Face search showed the BNB packaging. | Lightweight multimodal packaging comparison point. |

## Guardrails

- No runtime proof is claimed for the new candidates.
- These packages stay in research/runtime lanes only.
- Qwen3.7 remains watchlist-only until official open weights appear.
