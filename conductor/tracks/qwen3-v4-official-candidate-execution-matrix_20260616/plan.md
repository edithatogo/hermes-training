# Plan: Qwen3 v4 Official Candidate Execution Matrix

## Phase 1 - Matrix Builder

- [x] Task: read the official-candidate suite queue.
- [x] Task: derive execution status from existing suite preflights and the
  safety/refusal manifest.
- [x] Task: record SSD-backed output roots and completion artifacts.

## Phase 2 - Validation

- [x] Task: add a matrix validator that fails on missing, stale, or optimistic
  reports.
- [x] Task: add focused unit tests for blocked and ready suite states.
- [x] Task: add focused unit tests for the publication boundary.

## Phase 3 - Reports And Readiness

- [x] Task: generate
  `reports/benchmark/official-candidates/qwen3-v4-official-candidate-execution-matrix-20260616.json`.
- [x] Task: generate
  `reports/benchmark/official-candidates/qwen3-v4-official-candidate-execution-matrix-20260616.md`.
- [x] Task: wire the validator into `scripts/validate_readiness.py`.
- [x] Task: add this Conductor track to the registry.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: the matrix is generated, validator-backed, unit-tested, SSD-scoped,
  and wired into full readiness.
- Remaining gap: this is an execution-readiness artifact only. Official BFCL,
  coding, safety/refusal runtime scoring, and RULER still need scored artifacts
  before any broad benchmark claim.
- Decision: complete this setup track while keeping official benchmark coverage
  missing until scores are ingested.
