# Plan: Qwen3 V4 PEFT Colab Full Scorecard

## Phase 1 - Prepare

- [x] Task: Promote the Colab pilot script to support uploaded JSON config.
- [x] Task: Add a no-limit selected-task config manifest.

## Phase 2 - Execute

- [x] Task: Create a clean Colab T4 session.
- [x] Task: Upload the PEFT adapter tarball and no-limit config.
- [x] Task: Run the no-limit selected-task `lm_eval[hf]` scorecard.
- [x] Task: Record that JSON and harness result artifacts were not recoverable.
- [x] Task: Retry only after Colab keepalive permission is fixed or a
  persistent backend is selected.
- [x] Task: Stop or verify cleanup of the Colab session.

## Phase 3 - Reconcile

- [x] Task: Record the tracked full-scorecard report.
- [x] Task: If all five tasks score, update standard benchmark coverage.
- [x] Task: Run validation and close the track.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10 as a closed Colab route superseded by validated
  persistent-backend evidence.
- Evidence: the bounded limit-5 Colab PEFT route scored successfully across all
  selected tasks; the no-limit run launched on Colab T4 and reached harness
  execution.
- Gaps: Colab-specific no-limit JSON and harness result artifacts were not
  recoverable because the Colab session was pruned mid-run after keepalive
  permission failures. This is no longer a benchmark-coverage blocker because
  Kaggle kernel version 7 completed the same no-limit selected-task scorecard
  with public PEFT artifacts and passed the no-pending ingest gate.
- Decision: close the Colab full-scorecard track as superseded by Kaggle v7
  evidence. Do not retry Colab no-limit scoring until the keepalive permission
  issue is fixed or a new Colab-specific comparison is explicitly needed.
