# Plan: Kaggle Result Ingest Gate

## Phase 1 - Validator

- [x] Task: Add `scripts/validate_kaggle_result_ingest.py`.
- [x] Task: Support pending-artifact mode for pre-run readiness.
- [x] Task: Fail closed on limited, partial, missing-task, timeout, or non-SSD result artifacts.

## Phase 2 - Tests And Readiness

- [x] Task: Add unit tests for pending, passing, and limited-run failure cases.
- [x] Task: Wire the validator into `scripts/validate_readiness.py`.
- [x] Task: Generate tracked JSON and Markdown ingest reports.

## Phase 3 - Documentation

- [x] Task: Add this Conductor track.
- [x] Task: Update the Kaggle scorecard handoff notes with the ingest gate.

## Health Check

- Target: >= 9.8 / 10
- Current estimate: 9.8 / 10
- Evidence:
  - `tests/test_validate_kaggle_result_ingest.py` passes.
  - `scripts/validate_kaggle_result_ingest.py` emits `pending_artifacts` until a downloaded summary exists.
  - `scripts/validate_readiness.py` now includes the ingest gate.
- Remaining blocker: explicit Kaggle run approval and downloaded result artifacts.
