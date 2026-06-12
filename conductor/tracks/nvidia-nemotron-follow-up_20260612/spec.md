# Specification: NVIDIA Nemotron Follow-Up

## Overview

Capture the newest official NVIDIA Nemotron base/evaluator and speech-support
checkpoints that were not yet explicit in the machine-readable model radar.

## Scope

- Add `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-Base-BF16`.
- Add `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-GenRM`.
- Add `nvidia/nemotron-speech-streaming-en-0.6b`.
- Update the radar docs to reflect the NVIDIA follow-up scan.

## Out Of Scope

- No runtime proof.
- No training or benchmark claims.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new NVIDIA repos.
- The release scan notes mention the follow-up scan.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the additions are source-backed official repos from NVIDIA.
- Remaining gap: runtime proof remains a separate gate.
