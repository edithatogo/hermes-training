# Specification: ASR Support Follow-Up

## Overview

Capture the newest official ASR and transcription repos that are useful as
support lanes for Hermes-agent workflows.

## Scope

- Add `Qwen/Qwen3-ASR-1.7B`.
- Add `CohereLabs/cohere-transcribe-03-2026`.
- Add `nvidia/parakeet-tdt-0.6b-v3`.
- Update the radar docs so these remain support lanes, not Hermes chat targets.

## Out Of Scope

- No runtime proof.
- No training or benchmark claims.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new ASR repos.
- The release scan notes mention the ASR follow-up.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the additions are source-backed official repos from Qwen, Cohere, and NVIDIA.
- Remaining gap: runtime proof remains a separate gate.
