# Plan: Qwen3 V4 PEFT Colab Full Scorecard

## Phase 1 - Prepare

- [x] Task: Promote the Colab pilot script to support uploaded JSON config.
- [x] Task: Add a no-limit selected-task config manifest.

## Phase 2 - Execute

- [x] Task: Create a clean Colab T4 session.
- [x] Task: Upload the PEFT adapter tarball and no-limit config.
- [x] Task: Run the no-limit selected-task `lm_eval[hf]` scorecard.
- [ ] Task: Download JSON and harness result artifacts.
- [x] Task: Stop or verify cleanup of the Colab session.

## Phase 3 - Reconcile

- [x] Task: Record the tracked full-scorecard report.
- [ ] Task: If all five tasks score, update standard benchmark coverage.
- [ ] Task: Run validation and close the track.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 7.8 / 10 while blocked on long-running Colab session
  stability.
- Evidence: the bounded limit-5 Colab PEFT route scored successfully across all
  selected tasks; the no-limit run launched on Colab T4 and reached harness
  execution.
- Gaps: no-limit JSON and harness result artifacts were not recoverable because
  the Colab session was pruned mid-run after keepalive permission failures.
- Decision: keep full coverage blocked; retry only after fixing Colab keepalive
  permissions or moving the full run to persistent cloud execution.
