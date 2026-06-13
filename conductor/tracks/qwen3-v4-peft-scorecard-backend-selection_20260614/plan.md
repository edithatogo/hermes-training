# Plan: Qwen3 v4 PEFT Scorecard Backend Selection

## Phase 1: Selector

- [x] Task: add `scripts/select_scorecard_backend.py`.
- [x] Task: rank persistent backend candidates from the cloud unblock checklist.
- [x] Task: penalize Colab no-limit scorecard retries while keepalive/session
  pruning blockers remain.

## Phase 2: Validation

- [x] Task: add `scripts/validate_scorecard_backend_selection.py`.
- [x] Task: add unit tests for backend ranking and fail-closed semantics.
- [x] Task: wire the validator into `scripts/validate_readiness.py`.

## Phase 3: Reporting

- [x] Task: generate
  `reports/cloud/qwen3-v4-peft-scorecard-backend-selection-20260614.json`.
- [x] Task: generate
  `reports/cloud/qwen3-v4-peft-scorecard-backend-selection-20260614.md`.
- [x] Task: document that Kaggle is selected only as a gated route, not as an
  approved remote run.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: targeted tests and `validate_scorecard_backend_selection.py` pass.
- Gaps: no backend execution has been approved or launched.
