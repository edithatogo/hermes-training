# Plan: Nanbeige 4.1 3B Held-Out Envelope Diagnostic

## Phase 1: Held-Out Replay

- [x] Task: replay the existing held-out Nanbeige strict outputs through the
  constrained-envelope diagnostic runner.
- [x] Task: preserve the raw held-out baseline and constrained held-out result.
- [x] Task: keep the result non-promotional.

## Phase 2: Validation

- [x] Task: add `scripts/validate_nanbeige_heldout_envelope_report.py`.
- [x] Task: wire the validator into readiness.
- [x] Task: add unit coverage for rejecting promotional/full-pass reports.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: the tracked report preserves raw `1/8` and constrained `3/8`
  results, with SSD-backed full replay artifacts.
- Gaps: the held-out envelope result is still insufficient for promotion.
