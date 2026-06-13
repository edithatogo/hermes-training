# Plan: Qwen3 V4 PEFT Colab lm-eval Pilot

## Phase 1 - Harness

- [x] Task: Add a Colab `lm_eval[hf]` script for the converted PEFT adapter.
- [x] Task: Add the script to readiness syntax validation.

## Phase 2 - Execute

- [x] Task: Upload the adapter tarball to a Colab T4 session.
- [x] Task: Run the bounded selected-task pilot and download the JSON result.
- [x] Task: Stop or verify cleanup of the Colab session.

## Phase 3 - Reconcile

- [x] Task: Record a tracked report.
- [x] Task: Run focused validation and close the track.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10.
- Evidence: PEFT load smoke passed on Colab T4; the bounded selected-task
  `lm_eval[hf]` pilot scored all five selected tasks at `--limit 5` through the
  converted PEFT adapter.
- Gaps: full no-limit selected-task scorecard has not yet been run.
- Decision: The PEFT Colab route is viable; promote to a no-limit scorecard
  execution track.
