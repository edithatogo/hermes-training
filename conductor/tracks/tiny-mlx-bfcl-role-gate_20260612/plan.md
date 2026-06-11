# Plan: Tiny MLX BFCL Role Gate

## Phase 1: Shared Pilot Runs

- [x] Task: run MiniCPM5 1B MLX on the BFCL-style 3-case local pilot.
- [x] Task: run Qwen3.5 0.8B on the same pilot.
- [x] Task: run Qwen3.5 2B on the same pilot.

## Phase 2: Comparison

- [x] Task: compare pass rates, failure modes, and cache footprints.
- [x] Task: record a fail-closed role decision.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: all three candidates were tested under the same local MLX pilot
  harness and documented with raw SSD output paths.
- Gaps: all scored 0.000, so the next step is prompt-format repair, not
  promotion.
