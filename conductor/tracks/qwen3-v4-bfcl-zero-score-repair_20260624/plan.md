# Plan: Qwen3 v4 BFCL Zero-Score Repair

## Phase 1 - Evidence Capture

- [x] Task: Record selected-slice BFCL result.
    - [x] Overall selected-slice accuracy: `0.000`.
    - [x] Python Simple AST: `0.000`.
    - [x] Multiple AST: `0.000`.
    - [x] Parallel AST: `0.000`.
- [x] Task: Preserve generate/evaluate logs in Git.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Evidence Capture' (Protocol in workflow.md)

## Phase 2 - Failure Analysis

- [x] Task: Inspect raw BFCL result JSON for selected categories.
    - [x] Report: `reports/benchmark/official-candidates/qwen3-v4-bfcl-zero-score-failure-analysis-20260624.json`.
    - [x] Markdown: `reports/benchmark/official-candidates/qwen3-v4-bfcl-zero-score-failure-analysis-20260624.md`.
- [x] Task: Compare scorer expectations against the OpenAI-normalized endpoint output.
    - [x] Finding: current artifact contains endpoint/proxy failures and blank generations, so the `0.000` score is not clean model-quality evidence.
- [x] Task: Decide whether repair belongs in runtime/profile, model mapping, or adapter data.
    - [x] Decision: first repair is clean BFCL regeneration under a stable endpoint and low concurrency; defer adapter/runtime changes until clean outputs still fail.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Failure Analysis' (Protocol in workflow.md)

## Phase 3 - Minimal Rerun

- [ ] Task: Apply the selected repair.
- [ ] Task: Rerun selected BFCL categories.
- [ ] Task: Record score, logs, and publication boundary.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Minimal Rerun' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10 before marking complete.
- Current estimate: 8.0 / 10.
- Current blocker: selected-slice BFCL `0.000` is contaminated by stale endpoint
  failures and blank outputs. The next unblock is a clean selected-slice BFCL
  regeneration with `--num-threads 1`, archived stale output, endpoint/proxy logs,
  and zero upstream-error/blank-output rows before any model-quality promotion.
