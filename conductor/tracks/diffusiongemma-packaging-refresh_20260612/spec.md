# Specification: DiffusionGemma Packaging Refresh

## Overview

The Hermes radar needs to track fresh packaging variants separately from the
base release so runtime options stay explicit.

This refresh focuses on:

- `nvidia/diffusiongemma-26B-A4B-it-NVFP4`
- `mlx-community/diffusiongemma-26B-A4B-it-mxfp4`

## Scope

- Verify the current published status of the packaging variants.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, and `HANDOFF.md`.
- Record a concise scan report of the additions and guardrails.

## Out Of Scope

- No runtime proof claims for the new candidates.
- No training runs.
- No promotion to Hermes adapter targets.

## Acceptance Criteria

- The radar includes the fresh packaging variants.
- The docs keep them in research/runtime lanes.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is source-backed and preserves the lane boundary.
- Remaining gap: runtime proof is still separate for the packaging variants.
