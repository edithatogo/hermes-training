# Plan: Kaggle Kernel Contract Readiness

## Phase 1 - Contract Validator

- [x] Task: Add `scripts/validate_kaggle_kernel_contract.py`.
  - [x] Check staged metadata.
  - [x] Check staged scorecard config.
  - [x] Check dry-run execution gates.
  - [x] Check preflight quota visibility.
  - [x] Check runner artifact and claim-boundary text.

## Phase 2 - Reports

- [x] Task: Generate `reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.json`.
- [x] Task: Generate `reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.md`.

## Phase 3 - Readiness

- [x] Task: Add unit tests.
- [x] Task: Add validator to Python syntax checks.
- [x] Task: Add validator to full readiness.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.9 / 10
- Evidence: The staged Kaggle route has a passing, tracked no-execution contract before any kernel push.
- Validation: Kaggle contract tests, contract validator, Conductor consistency, and full readiness are required before commit.
- Gaps: No Kaggle kernel was pushed or run.
- Decision: Complete. Kaggle is better prepared while keeping execution approval-gated.
