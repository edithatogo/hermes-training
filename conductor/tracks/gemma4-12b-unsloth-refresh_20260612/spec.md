# Specification: Gemma 4 12B Unsloth Refresh

## Overview

The Gemma 4 12B family now has verified Unsloth GGUF and QAT packaging that
matters for Hermes local runtime work on a 32GB Mac.

This refresh focuses on:

- `google/gemma-4-12B-it`
- `google/gemma-4-12B`
- `unsloth/gemma-4-12b-it-GGUF`
- `unsloth/gemma-4-12B-it-qat-GGUF`

## Scope

- Verify the current published status of the Gemma 4 12B native and Unsloth
  packaging lanes.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, `HANDOFF.md`, and the
  current release scan notes.
- Record a concise model-radar report explaining the 12B packaging options.

## Out Of Scope

- No training runs.
- No runtime proof claims.
- No publication or benchmark claims.

## Acceptance Criteria

- The radar includes the fresh Gemma 4 12B Unsloth packaging entries.
- The docs keep the family in runtime/packaging lanes.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the packaging is source-backed and immediately relevant to the Mac
  runtime lane.
- Remaining gap: runtime proof for the new packaging.
