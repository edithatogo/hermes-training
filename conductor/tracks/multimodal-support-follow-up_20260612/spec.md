# Specification: Multimodal Support Follow-Up

## Overview

Capture the newest multimodal repos that are relevant as support lanes for
Hermes-agent workflows across text, image, audio, and video.

## Scope

- Add `Qwen/Qwen3-Omni-30B-A3B-Instruct`.
- Add `Qwen/Qwen3-Omni-30B-A3B-Captioner`.
- Add `microsoft/Phi-4-multimodal-instruct`.
- Update the radar docs so these remain support lanes, not Hermes text targets.

## Out Of Scope

- No runtime proof.
- No training or benchmark claims.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new multimodal repos.
- The release scan notes mention the multimodal follow-up.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the additions are source-backed and directly useful for broad multimodal support.
- Remaining gap: runtime proof remains a separate gate.
