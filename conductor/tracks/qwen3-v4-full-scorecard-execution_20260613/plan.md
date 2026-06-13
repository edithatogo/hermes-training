# Plan: Qwen3 V4 Full Selected-Task Scorecard Execution

## Phase 1 - Preflight

- [x] Task: Validate the full scorecard manifest.
  - [x] Confirm the command is no-limit and SSD-backed.
  - [x] Confirm official benchmark manifest validation passes.
- [x] Task: Confirm output root and benchmark environment exist.

## Phase 2 - Execute Resumable Scorecard

- [x] Task: Run `scripts/run_mlx_lm_eval.py` with the full selected task set.
  - [x] Preserve partial `summary.json`, `results.json`, and Markdown report updates.
  - [x] Stop and record a concrete local blocker when the first task did not complete after 731.827 seconds.

## Phase 3 - Reconcile Evidence

- [x] Task: If the run scores every task, regenerate standard coverage and update the `lm-eval-selected` status.
  - [x] Not applicable: the run did not score any complete task.
- [x] Task: If the run blocks, record the blocker and keep broad benchmark claims blocked.
- [x] Task: Run focused tests and hub readiness validation.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: manifest validation and dry-run preflight pass; output root is SSD-backed; `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613.md` records the interrupted local full-run attempt after 731.827 seconds with 0/5 tasks complete.
- Gaps: full selected-task scores are still missing and broad benchmark claims remain blocked.
- Decision: Complete as a local execution attempt and routing decision. Move the full scorecard to Colab/Azure/offload or explicitly resume a long local run.
