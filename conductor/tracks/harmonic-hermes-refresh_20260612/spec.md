# Specification: Harmonic Hermes Refresh

## Overview

Hermes-style local work now has a new agentic fine-tune family worth tracking:
Harmonic-9B and Harmonic-Hermes-9B.

This refresh focuses on:

- `DJLougen/Harmonic-9B`
- `DJLougen/Harmonic-Hermes-9B-GGUF`
- `mradermacher/Harmonic-Hermes-9B-i1-GGUF`

## Scope

- Verify the current published status of the Harmonic backbone and agentic
  fine-tune family.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, `HANDOFF.md`, and the
  current release scan notes.
- Record a concise model-radar report explaining why the family belongs in the
  Hermes local runtime lane.

## Out Of Scope

- No training runs.
- No runtime proof claims.
- No publication or benchmark claims.

## Acceptance Criteria

- The radar includes Harmonic-9B and Harmonic-Hermes-9B packaging.
- The docs keep the family in the runtime/teacher lanes.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the family is source-backed, open-weight, and directly aligned with
  the Hermes tool-use lane.
- Remaining gap: runtime proof on the Mac lane.
