# Specification: Gemma 4 31B Community GGUF Refresh

## Overview

Capture the fresh `bartowski/google_gemma-4-31B-it-GGUF` packaging lane that
surfaced in the latest Hugging Face search and is relevant to Hermes local
Gemma 4 31B packaging comparisons.

## Scope

- Add `bartowski/google_gemma-4-31B-it-GGUF`.
- Keep the lane clearly separated from the official QAT and LM Studio GGUF packs.

## Out Of Scope

- No runtime proof in this slice.
- No fine-tuning or benchmark claim.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new community GGUF entry.
- The release scan notes mention the new packaging lane.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the packaging lane is source-backed and directly useful for local
  Gemma 4 31B comparison work.
- Remaining gap: runtime proof remains separate.
