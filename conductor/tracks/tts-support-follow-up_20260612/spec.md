# Specification: TTS Support Follow-Up

## Overview

Capture the newest official speech-generation repo and its Mac-local packaging so
the radar covers the outbound speech side of Hermes-agent workflows too.

## Scope

- Add `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`.
- Add `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16`.
- Update the radar docs so these remain speech-support lanes, not Hermes chat targets.

## Out Of Scope

- No runtime proof.
- No training or benchmark claims.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new TTS repos.
- The release scan notes mention the TTS follow-up.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the additions are source-backed official and MLX-packaged Qwen speech repos.
- Remaining gap: runtime proof remains a separate gate.
