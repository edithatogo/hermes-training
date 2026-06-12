# Specification: Hermes-Qwen3.5 SFT v7 Refresh

## Overview

Fresh Hermes-Qwen3.5 SFT v7 packs surfaced on Hugging Face and are directly
relevant to the repo's local Hermes runtime lane.

This refresh focuses on:

- `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`
- `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7`
- `mkadrlik/hermes-Qwen3.5-2B-SFT-v7`
- `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh`
- `mkadrlik/Hermes-27B-SFT-v7`

## Scope

- Verify the current published status of the Hermes-Qwen3.5 SFT v7 packs.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, `HANDOFF.md`, and the
  current release scan notes.
- Record a concise report explaining the local runtime and teacher lanes.

## Out Of Scope

- No training runs.
- No runtime proof claims.
- No benchmark claims.

## Acceptance Criteria

- The radar includes the Hermes-Qwen3.5 SFT v7 packs.
- The docs keep them in runtime/helper lanes.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the lane is source-backed, Hermes-specific, and directly useful.
- Remaining gap: runtime proof and prompt-format behavior on each pack.
