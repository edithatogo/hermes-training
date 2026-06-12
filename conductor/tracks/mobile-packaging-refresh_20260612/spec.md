# Specification: Mobile Packaging Refresh

## Overview

The Hermes radar needs to capture fresh mobile/runtime packaging variants
separately from the base release tracks.

This refresh focuses on:

- `google/gemma-4-E2B-it-qat-mobile-transformers`
- `google/gemma-4-E4B-it-qat-mobile-transformers`
- `openbmb/MiniCPM-V-4.6-BNB`

## Scope

- Verify the current published status of the packaging variants.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, and `HANDOFF.md`.
- Record a concise scan report of the additions and guardrails.

## Out Of Scope

- No runtime proof claims for the new candidates.
- No training runs.
- No promotion to Hermes adapter targets.

## Acceptance Criteria

- The radar includes the fresh mobile/BNB packaging variants.
- The docs keep them in research/runtime lanes.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is source-backed and preserves the lane boundary.
- Remaining gap: runtime proof is still separate for the packaging variants.
