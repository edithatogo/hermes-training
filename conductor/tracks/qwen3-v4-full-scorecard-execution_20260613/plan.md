# Plan: Qwen3 V4 Full Selected-Task Scorecard Execution

## Phase 1 - Preflight

- [x] Task: Validate the full scorecard manifest.
  - [x] Confirm the command is no-limit and SSD-backed.
  - [x] Confirm official benchmark manifest validation passes.
- [x] Task: Confirm output root and benchmark environment exist.

## Phase 2 - Execute Resumable Scorecard

- [~] Task: Run `scripts/run_mlx_lm_eval.py` with the full selected task set.
  - [ ] Preserve partial `summary.json`, `results.json`, and Markdown report updates.
  - [ ] Resume from existing task checkpoints if the run is interrupted.

## Phase 3 - Reconcile Evidence

- [ ] Task: If the run scores every task, regenerate standard coverage and update the `lm-eval-selected` status.
- [ ] Task: If the run blocks, record the blocker and keep broad benchmark claims blocked.
- [ ] Task: Run focused tests and hub readiness validation.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 8.9 / 10 while execution is in progress
- Evidence: manifest validation and dry-run preflight pass; output root is SSD-backed.
- Gaps: full scorecard is not yet scored.
- Decision: Keep the track in progress until the run scores or records a concrete blocker.
