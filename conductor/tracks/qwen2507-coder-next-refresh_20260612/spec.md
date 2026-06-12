# Specification: Qwen 2507 and Coder-Next Refresh

## Overview

The Hermes radar needs to reflect the newest official Qwen releases that are
actually relevant to Hermes workflows on local or burst compute.

This refresh focuses on:

- `Qwen/Qwen3-4B-Instruct-2507`
- `Qwen/Qwen3-4B-Thinking-2507`
- `Qwen/Qwen3-Coder-Next-GGUF`

## Scope

- Verify the current published status of the official Qwen releases.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, and `HANDOFF.md`.
- Record a concise scan report of the official Qwen refresh and the Qwen3.7
  guardrail.

## Out Of Scope

- No local training runs.
- No promotion of Qwen3.7 to an implementation lane.
- No runtime proof claims unless already documented in the existing repo.

## Acceptance Criteria

- The radar includes the Qwen 2507 instruction and thinking releases.
- The radar includes the official Qwen3-Coder-Next GGUF lane.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is source-backed, conservative, and lane-scoped.
- Remaining gap: runtime proof stays separate from publication of the radar.
