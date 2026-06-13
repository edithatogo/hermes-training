# Plan: Constrained Envelope Repair Plan

## Phase 1: Evidence Classification

- [x] Task: read the completed prompt/profile repair result index.
- [x] Task: inspect source `results.jsonl` artifacts from the SSD evaluation root.
- [x] Task: classify exact-call-plus-extra-text failures separately from malformed
  or empty outputs.

## Phase 2: Report And Guardrails

- [x] Task: generate
  `reports/benchmark/coverage/constrained-envelope-repair-plan-20260614.json`.
- [x] Task: generate
  `reports/benchmark/coverage/constrained-envelope-repair-plan-20260614.md`.
- [x] Task: add a validator that enforces source evidence, strict scoring, and
  non-promotion boundaries.
- [x] Task: wire the validator into full readiness.

## Phase 3: Validation

- [x] Task: add unit tests for ranking and validation behavior.
- [x] Task: run focused tests and constrained-envelope plan validation.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.8 / 10`
- Evidence: Nanbeige is ranked from observed per-case outputs rather than model
  preference, and the validator prevents score-only promotion drift.
- Gaps: no runtime-wrapper proof has been executed yet.
