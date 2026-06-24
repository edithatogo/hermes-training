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
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Failure Analysis' (Protocol in workflow.md)

## Phase 3 - Minimal Rerun

- [x] Task: Apply the selected repair.
    - [x] Use stable MLX endpoint `127.0.0.1:8097` plus normalizing proxy `127.0.0.1:8098`.
    - [x] Use fresh SSD-backed output root `qwen3-v4-peft-official-bfcl-clean-rerun-20260624`.
- [x] Task: Rerun selected BFCL categories as a gated clean attempt.
    - [x] Launch with `--num-threads 1`, `--skip-server-setup`, and `--include-input-log`.
    - [x] Stop after `10/10` clean-endpoint rows were blank to avoid spending the full selected-slice budget on unusable evidence.
- [x] Task: Record score, logs, and publication boundary.
    - [x] Report: `reports/benchmark/official-candidates/qwen3-v4-bfcl-clean-rerun-20260624.md`.
    - [x] Gate result: `upstream_error_rows == 0`, `blank_output_rows == 10`, overall accuracy `0.00%`.
    - [x] Publication boundary: evidence-only; not full BFCL or model-quality evidence.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Minimal Rerun' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10 before marking complete.
- Current estimate: 8.4 / 10.
- Current blocker: the stable endpoint/proxy rerun cleared upstream errors, but
  the clean attempt produced blank model outputs (`10/10` rows). The next
  unblock is repairing BFCL completion behavior before another selected-slice
  regeneration; do not promote the score as model-quality evidence.
