# Plan: Qwen3 v8 Safety/Refusal Wrapper + Contrastive Repair

## Phase 1 - Evidence-Locked Queue

- [ ] Task: Inspect the v7 repair-run report and raw safety/refusal summary.
    - [ ] Confirm strict pass `0.375`, empty-think prefix cases `8`, and residual failure count `3`.
    - [ ] Confirm residual IDs are `heldout-argument-correctness-lab-order`, `heldout-invalid-tool-handling-security`, and `safety-refusal-exfiltrate-secret`.
- [ ] Task: Add a generated v8 repair queue report.
    - [ ] Include v7 source metrics and the hard "do not publish v7 weights" boundary.
    - [ ] Split repairs into wrapper-removal/profile, refusal contrastive data, and schema-correct tool-call repair.
    - [ ] Store JSON and Markdown reports under `reports/benchmark/official-candidates/`.
- [ ] Task: Add focused tests for the queue/report builder.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Evidence-Locked Queue' (Protocol in workflow.md)

## Phase 2 - Repair Materialization

- [ ] Task: Materialize the next repair inputs.
    - [ ] Add wrapper-removal/profile experiment inputs without weakening strict scoring.
    - [ ] Add contrastive refusal rows for security/exfiltration prompts that avoid forbidden markers.
    - [ ] Add a schema-correct repair row for `heldout-argument-correctness-lab-order`.
- [ ] Task: Add validation for materialized data/profile.
    - [ ] Fail on held-out leakage into training data.
    - [ ] Fail if refusal targets contain tool calls or forbidden markers.
    - [ ] Fail if adapter output paths collide with v7 publication artifacts.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Repair Materialization' (Protocol in workflow.md)

## Phase 3 - Bounded Rerun And Gate Decision

- [ ] Task: Train or run the smallest bounded v8 repair experiment.
    - [ ] Keep adapter weights ignored under `gemma4/experiments/`.
    - [ ] Keep raw logs and benchmark outputs on `/Volumes/PortableSSD`.
- [ ] Task: Rerun the pinned 8-case safety/refusal suite.
    - [ ] Require strict pass rate `1.000`.
    - [ ] Require empty-think prefix cases `0`.
    - [ ] Require residual strict failures `0`.
- [ ] Task: Ingest result evidence and update the official-candidate matrix.
    - [ ] Keep publication blocked if any target gate fails.
    - [ ] Add HF private artifact tracking only for evidence, not public weights.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Bounded Rerun And Gate Decision' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10 before marking complete.
- Current estimate: 8.8 / 10.
- Current blocker: implementation is not started; this track currently defines
  the next repair path from scored v7 evidence.
