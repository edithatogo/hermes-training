# Specification: Qwen3.6 35B 2-bit MLX Refresh

## Overview

ManiacLabs published a fresh 2-bit MLX pack for Qwen3.6 35B that is tagged for
function-calling, tool-calling, and agentic use on Apple Silicon.

This refresh focuses on:

- `ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming`
- `Qwen/Qwen3.6-35B-A3B`
- `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX`
- `deepsweet/Qwen3.6-35B-A3B-MLX-oQ4`

## Scope

- Verify the current published status of the ManiacLabs 2-bit MLX pack.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, `HANDOFF.md`, and the
  current release scan notes.
- Record a concise report explaining the local runtime comparison point.

## Out Of Scope

- No training runs.
- No runtime proof claims.
- No benchmark claims.

## Acceptance Criteria

- The radar includes the ManiacLabs 2-bit MLX pack.
- The docs keep it in the local-runtime lane.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the pack is source-backed and directly useful for Apple Silicon.
- Remaining gap: runtime proof and tool-call behavior on the target stack.
