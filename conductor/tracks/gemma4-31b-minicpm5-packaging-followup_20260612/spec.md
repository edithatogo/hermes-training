# Specification: Gemma 4 31B and MiniCPM5-1B Packaging Follow-up

## Overview

Capture the newest community and official packaging lanes surfaced in the live
Hugging Face refresh: `unsloth/gemma-4-31B-it-GGUF`,
`ggml-org/gemma-4-31B-it-GGUF`, and `openbmb/MiniCPM5-1B-GGUF`.

## Scope

- Add the new Gemma 4 31B GGUF packaging lanes.
- Add the official MiniCPM5-1B GGUF lane.
- Keep `Abiray/MiniCPM5-1B-GGUF` documented as a community alternate only.
- Update the current release scan and the project-level model radar summary.

## Out Of Scope

- No runtime proof in this slice.
- No fine-tuning or benchmark claims.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new packaging entries.
- The release scan notes mention the new packaging lanes.
- Project docs and track registry reflect the follow-up refresh cleanly.
- Validation passes without whitespace or candidate-registry errors.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the new lanes are source-backed, locally relevant, and directly
  improve model-selection coverage for Hermes-adjacent workflows.
- Remaining gap: runtime proof remains separate.
