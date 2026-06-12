# Specification: Support Lane Surface Refresh

## Overview

Capture the newest non-core support lanes surfaced in the latest Hugging Face
refresh: `deepseek-ai/DeepSeek-V4-Pro`, `nvidia/LocateAnything-3B`, and
`bosonai/higgs-audio-v3-tts-4b`.

## Scope

- Add the new DeepSeek V4 Pro teacher lane.
- Add the NVIDIA visual grounding lane for helper workflows.
- Add the Boson AI speech/voice-agent lane for future audio workflows.
- Update the current release scan and project docs so the lanes stay visible.

## Out Of Scope

- No runtime proof in this slice.
- No training or benchmark claims.
- No publication or adapter promotion.

## Acceptance Criteria

- The candidate list contains the new support lanes with sensible roles.
- The release scan mentions the new support lanes.
- The handoff and roadmap docs reflect the new model surface.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.5 / 10`
- Evidence: the models are source-backed and useful for Hermes-adjacent support,
  teacher, and multimodal workflows.
- Remaining gap: runtime proof is intentionally out of scope.
