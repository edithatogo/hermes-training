# Plan: Free Container Probe Readiness Validator

## Phase 1 - Validator

- [x] Task: Add `scripts/validate_free_container_account_probe.py`.
  - [x] Check required sections and safety boundary.
  - [x] Reject obvious secret strings and execution commands.
  - [x] Normalize whitespace for wrapped Markdown text.

## Phase 2 - Tests

- [x] Task: Add unit tests for the validator.
  - [x] Passing report.
  - [x] Missing safety boundary and secret failure.

## Phase 3 - Readiness

- [x] Task: Add the validator to Python syntax checks.
- [x] Task: Add the validator to the full readiness sequence.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.9 / 10
- Evidence: Full readiness now verifies the free-container probe report and its no-job/no-paid-compute boundary.
- Validation: Validator tests, probe validator, Conductor consistency, and full readiness are required before commit.
- Gaps: The probe was not rerun in this track.
- Decision: Complete. Account-state documentation is now covered by readiness.
