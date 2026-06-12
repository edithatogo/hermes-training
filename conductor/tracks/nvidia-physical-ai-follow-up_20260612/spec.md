# Specification: NVIDIA Physical-AI Follow-Up

## Overview

Capture the newest NVIDIA physical-AI and world-model support lanes that
appeared in the current official search, so the radar reflects the broader
Hermes-adjacent ecosystem without pretending they are chat models.

## Scope

- Add `nvidia/instant-nurec`.
- Add `nvidia/omni-dreams-models`.
- Update the radar docs so these remain support lanes, not Hermes text targets.

## Out Of Scope

- No runtime proof.
- No training or benchmark claims.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new NVIDIA support lanes.
- The release scan notes mention the follow-up scan.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the additions are source-backed official NVIDIA repos.
- Remaining gap: runtime proof remains a separate gate.
