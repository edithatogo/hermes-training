# Plan: Qwen3 V4 PEFT Colab Load Smoke

## Phase 1 - Package

- [x] Task: Add a Colab load-smoke script for an uploaded PEFT tarball.
- [x] Task: Create the adapter tarball from the converted PEFT output.

## Phase 2 - Execute

- [x] Task: Start a Colab T4 session and upload the tarball.
- [x] Task: Run the load-smoke script and download/record the result.
- [x] Task: Stop the Colab session.

## Phase 3 - Reconcile

- [x] Task: Record the route decision in a tracked report.
- [x] Task: Run focused validation and close the track.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: `reports/colab/qwen3-v4-peft-load-smoke-20260613.md` records a Colab T4 4-bit `Qwen/Qwen3-4B` + converted PEFT adapter load and short generation.
- Gaps: full selected-task `lm-eval` has not been run for the converted PEFT candidate.
- Decision: Close load smoke as passed and open a follow-on Colab selected-task scorecard execution track.
