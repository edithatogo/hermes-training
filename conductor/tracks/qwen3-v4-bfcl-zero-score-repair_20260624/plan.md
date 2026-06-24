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

- [ ] Task: Inspect raw BFCL result JSON for selected categories.
- [ ] Task: Compare scorer expectations against the OpenAI-normalized endpoint output.
- [ ] Task: Decide whether repair belongs in runtime/profile, model mapping, or adapter data.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Failure Analysis' (Protocol in workflow.md)

## Phase 3 - Minimal Rerun

- [ ] Task: Apply the selected repair.
- [ ] Task: Rerun selected BFCL categories.
- [ ] Task: Record score, logs, and publication boundary.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Minimal Rerun' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10 before marking complete.
- Current estimate: 7.0 / 10.
- Current blocker: selected-slice BFCL is runnable and scored, but accuracy is
  `0.000`; raw-output failure analysis is still needed before another rerun.
