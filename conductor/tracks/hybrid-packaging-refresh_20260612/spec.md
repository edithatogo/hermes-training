# Specification: Hybrid Attention and Quantized Packaging Refresh

## Overview

The Hermes radar needs a small follow-up pass for a hybrid-attention long
context model and a couple of quantized packaging variants.

This refresh focuses on:

- MiniCPM-SALA as a sparse/linear-attention long-context research lane
- Gemma 4 31B-it NVFP4 packaging as a cloud packaging comparison point
- DeepSeek-V4-Flash-Base as a long-context base packaging reference

## Scope

- Verify the current published status of the new candidate IDs.
- Add the verified candidates to `MODEL_CANDIDATES.yaml`.
- Update `FUTURE_MODELS.md` and `HANDOFF.md` with the new guidance.
- Record a concise scan report of the additions and guardrails.

## Out Of Scope

- No runtime proof claims for the new candidates.
- No training runs.
- No promotion of the new models to default local fine-tune targets.

## Acceptance Criteria

- The radar includes the new hybrid-attention and packaging candidates.
- The docs make clear these are teacher/runtime or specialist-only lanes.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is source-backed and keeps the candidates in
  specialist/runtime lanes.
- Remaining gap: runtime proof is still separate for every candidate.
