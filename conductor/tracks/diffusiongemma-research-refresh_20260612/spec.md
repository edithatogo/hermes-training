# Specification: DiffusionGemma Research Refresh

## Overview

The Hermes radar should record new diffusion-family releases separately from
normal Hermes adapter work so the role boundary stays explicit.

This refresh focuses on:

- `google/diffusiongemma-26B-A4B-it` as a fresh diffusion-family release
- a research/runtime note in the model radar

## Scope

- Verify the current published status of the candidate repo.
- Update `MODEL_CANDIDATES.yaml` and `FUTURE_MODELS.md` with the diffusion
  lane note.
- Record a concise scan report of the addition and guardrails.

## Out Of Scope

- No runtime proof claims for the new candidate.
- No training runs.
- No promotion to Hermes adapter targets.

## Acceptance Criteria

- The radar includes DiffusionGemma as a research/runtime lane.
- The docs make clear it is not a Hermes adapter target.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is source-backed and preserves the lane boundary.
- Remaining gap: runtime proof is still separate for the diffusion lane.
