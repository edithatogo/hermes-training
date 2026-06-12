# Specification: Gemma 4 E2B-it Packaging Refresh

## Overview

Capture the official Gemma 4 E2B-it instruction-tuned repo and the newest
small packaging lanes that make it practical on Mac-local and specialist
runtime paths.

## Scope

- Add `google/gemma-4-E2B-it`.
- Add `litert-community/gemma-4-E2B-it-litert-lm`.
- Add `mlx-community/gemma-4-e2b-it-4bit`.
- Keep the existing E2B q4_0 GGUF runtime proof separate from this packaging
  refresh.
- Update the radar docs so the E2B-it lane is clearly treated as the smallest
  practical Gemma 4 comparison point.

## Out Of Scope

- No new runtime proof in this slice.
- No fine-tuning or benchmark claim.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable radar includes the new Gemma 4 E2B-it entries.
- The release scan notes mention the new E2B-it packaging lane.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the official E2B-it repo and packaging lanes are source-backed and
  directly useful for the Mac-local helper path.
- Remaining gap: runtime proof remains a separate gate.
