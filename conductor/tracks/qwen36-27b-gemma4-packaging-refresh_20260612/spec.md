# Specification: Qwen3.6-27B and Gemma 4 Packaging Refresh

## Overview

The Hermes radar needs a denser Qwen3.6 comparison point and a tighter view
of the current Gemma 4 packaging surface.

This refresh focuses on:

- Qwen/Qwen3.6-27B as the new dense small-model frontier point
- Qwen3.6-27B FP8, GGUF, and MLX packaging
- the current Gemma 4 12B / 31B packaging surface from Google and Unsloth

## Scope

- Verify the current published status of the new Qwen3.6-27B and Gemma 4
  packaging candidates.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, and `HANDOFF.md` with
  the new guidance.
- Record a concise scan report of the additions and guardrails.

## Out Of Scope

- No runtime proof claims for the new candidates.
- No training runs.
- No promotion of the new models to default local fine-tune targets.

## Acceptance Criteria

- The radar reflects Qwen3.6-27B as a current dense frontier candidate.
- The docs clearly separate the new candidates into runtime or teacher lanes.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is source-backed and keeps the candidates in
  specialist/runtime lanes.
- Remaining gap: runtime proof is still separate for every candidate.
