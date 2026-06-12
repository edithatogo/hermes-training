# Specification: Gemma 4 31B and MiniCPM-o 4.5 Packaging Refresh

## Overview

Capture the explicit `google/gemma-4-31B-it-qat-q4_0-gguf` and
`openbmb/MiniCPM-o-4_5-gguf` packaging lanes that surfaced in the latest
Hugging Face search and are relevant to Hermes local packaging comparisons.

## Scope

- Add `google/gemma-4-31B-it-qat-q4_0-gguf`.
- Add `openbmb/MiniCPM-o-4_5-gguf`.
- Keep both lanes clearly separated from their base model cards.

## Out Of Scope

- No runtime proof in this slice.
- No fine-tuning or benchmark claim.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new packaging entries.
- The release scan notes mention the new packaging lanes.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the explicit packaging lanes are source-backed and directly useful
  for local comparison and runtime triage.
- Remaining gap: runtime proof stays separate.
