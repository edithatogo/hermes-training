# Plan: Qwen3 v8 Safety/Refusal Wrapper + Contrastive Repair

## Phase 1 - Evidence-Locked Queue

- [x] Task: Inspect the v7 repair-run report and raw safety/refusal summary.
    - [x] Confirm strict pass `0.375`, empty-think prefix cases `8`, and residual failure count `3`.
    - [x] Confirm residual IDs are `heldout-argument-correctness-lab-order`, `heldout-invalid-tool-handling-security`, and `safety-refusal-exfiltrate-secret`.
- [x] Task: Add a generated v8 repair queue/report.
    - [x] Include v7 source metrics and the hard "do not publish v7 weights" boundary.
    - [x] Split repairs into wrapper-removal/profile, exact free-text copying, refusal contrastive data, and schema-correct tool-call repair.
    - [x] Store JSON and Markdown reports under `reports/benchmark/official-candidates/`.
- [x] Task: Add focused tests for the queue/report builder.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Evidence-Locked Queue' (Protocol in workflow.md)

## Phase 2 - Repair Materialization

- [x] Task: Materialize the next repair inputs.
    - [x] Add wrapper-removal/profile experiment inputs without weakening strict scoring.
    - [x] Add contrastive refusal rows for security/exfiltration prompts that avoid forbidden markers.
    - [x] Add exact free-text argument-copying rows.
    - [x] Add a schema-correct repair row for `heldout-argument-correctness-lab-order`.
- [x] Task: Add validation for materialized data/profile.
    - [x] Fail on held-out leakage into training data.
    - [x] Fail if refusal targets contain tool calls or forbidden markers.
    - [x] Fail if adapter output paths collide with v7 publication artifacts.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Repair Materialization' (Protocol in workflow.md)

## Phase 3 - Bounded Rerun And Gate Decision

- [x] Task: Train or run the smallest bounded v8 repair experiment.
    - [x] Keep adapter weights ignored under `gemma4/experiments/`.
    - [x] Keep raw logs and benchmark outputs on `/Volumes/PortableSSD`.
- [x] Task: Rerun the pinned 8-case safety/refusal suite.
    - [x] Record strict pass rate `0.375`; target `1.000` was not met.
    - [x] Record empty-think prefix cases `8`; target `0` was not met.
    - [x] Record residual strict failures `2`; target `0` was not met.
- [x] Task: Ingest result evidence and update the official-candidate evidence.
    - [x] Keep publication blocked because the target gates failed.
    - [x] Keep HF artifact tracking out of public weights; HF upload remains blocked by auth/publication review.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Bounded Rerun And Gate Decision' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10 before marking complete.
- Current estimate: 9.6 / 10.
- Current blocker: model gates remain failed, but the track has completed its
  bounded v8 repair run and fail-closed evidence capture. Next work should be a
  separate v9/runtime-profile repair focused on suppressing the empty
  `<think>` wrapper at generation time and avoiding unavailable tool-name echo
  in refusals.
