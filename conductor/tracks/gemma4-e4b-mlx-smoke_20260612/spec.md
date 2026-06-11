# Spec: Gemma 4 E4B MLX Runtime And Role Smoke

## Problem

The raw official Gemma 4 E2B GGUF proof loaded but returned only end-of-text.
The next useful local lane was the E4B QAT MLX package, because MLX tests the
native Apple Silicon path and may avoid GGUF prompt/EOG quirks.

## Scope

- Acquire `mlx-community/gemma-4-E4B-it-qat-4bit` to the SSD-backed Hugging Face
  cache.
- Run a one-case direct MLX loglikelihood smoke.
- Run the existing 3-case BFCL-style local pilot.
- Record pass/fail evidence without promoting the model.
- Update the runtime proof queue, model radar, future model notes, handoff, and
  Conductor registry.

## Out Of Scope

- No fine-tuning.
- No E4B/E2B publication.
- No broad standard benchmark or leaderboard claim.
- No multimodal projector work.

## Acceptance Criteria

- Artifact and outputs remain under `/Volumes/PortableSSD`.
- Direct MLX load/scoring either passes or fails with an explicit blocker.
- BFCL-style role gate result is recorded.
- Project validations pass.
