# Specification: Nemotron Support Model Refresh

## Overview

The radar should also carry newer specialist support models that shape agent
deployment boundaries, especially moderation and streaming speech.

This refresh focuses on:

- Nemotron 3.5 content safety
- Nemotron 3.5 streaming ASR
- the distinction between text-generation Hermes lanes and specialist support
  lanes

## Scope

- Verify the current published status of the Nemotron support releases.
- Add the verified support models to `MODEL_CANDIDATES.yaml`.
- Update `FUTURE_MODELS.md` and `HANDOFF.md` with the support-lane guidance.
- Record a concise report of the additions.

## Out Of Scope

- No runtime proof claims for the new support models.
- No training runs.
- No promotion to Hermes text-generation defaults.

## Acceptance Criteria

- The radar includes the Nemotron safety and ASR support models.
- The docs clearly separate support lanes from Hermes text lanes.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.5 / 10`
- Evidence: the refresh is source-backed and respects the support/runtime
  boundary.
- Remaining gap: runtime proof is still separate for each support model.
