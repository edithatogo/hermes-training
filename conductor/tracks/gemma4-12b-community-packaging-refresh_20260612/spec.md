# Specification: Gemma 4 12B Community Packaging Refresh

## Overview

The Gemma 4 12B family now has additional community GGUF packagers and an
abliterated uncensored base lane that matter for Hermes local runtime work.

This refresh focuses on:

- `batiai/gemma-4-12B-it-GGUF`
- `OpenYourMind/gemma-4-12B-it-abliterated-uncensored`
- `DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF`

## Scope

- Verify the current published status of the community Gemma 4 12B packaging
  and base lanes.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, `HANDOFF.md`, and the
  current release scan notes.
- Record a concise model-radar report explaining the community packaging
  comparison points.

## Out Of Scope

- No training runs.
- No runtime proof claims.
- No publication or benchmark claims.

## Acceptance Criteria

- The radar includes the community Gemma 4 12B packaging entries.
- The docs keep the family in runtime/packaging lanes.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the lanes are source-backed and give concrete Mac-local packaging
  alternatives.
- Remaining gap: runtime proof for each packager.
