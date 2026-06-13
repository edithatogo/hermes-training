# Plan: Nanbeige 4.1 3B Constrained Envelope Diagnostic

## Phase 1: Diagnostic Runner

- [x] Task: add `scripts/run_constrained_envelope_diagnostic.py`.
- [x] Task: add unit tests for tool-call selection and refusal sentence selection.
- [x] Task: keep the runner replay-only with no model download or endpoint launch.

## Phase 2: Evidence Capture

- [x] Task: run the diagnostic against the existing Nanbeige strict repair output.
- [x] Task: write full replay artifacts under `/Volumes/PortableSSD/hermes-evals`.
- [x] Task: write compact tracked JSON and Markdown reports under
  `reports/benchmark/constrained-envelope/`.

## Phase 3: Validation

- [x] Task: add `scripts/validate_constrained_envelope_diagnostic_report.py`.
- [x] Task: wire the validator into full readiness.
- [x] Task: run focused tests and full readiness.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.8 / 10`
- Evidence: replay artifacts preserve the raw `0/3` baseline and constrained
  `3/3` diagnostic result with no promotion claim.
- Gaps: held-out runtime-wrapper proof remains separate follow-on work.
