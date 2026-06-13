# Plan: Qwen3 V4 PEFT Colab Full Scorecard

## Phase 1 - Prepare

- [x] Task: Promote the Colab pilot script to support uploaded JSON config.
- [x] Task: Add a no-limit selected-task config manifest.

## Phase 2 - Execute

- [ ] Task: Create a clean Colab T4 session.
- [ ] Task: Upload the PEFT adapter tarball and no-limit config.
- [ ] Task: Run the no-limit selected-task `lm_eval[hf]` scorecard.
- [ ] Task: Download JSON and harness result artifacts.
- [ ] Task: Stop or verify cleanup of the Colab session.

## Phase 3 - Reconcile

- [ ] Task: Record the tracked full-scorecard report.
- [ ] Task: If all five tasks score, update standard benchmark coverage.
- [ ] Task: Run validation and close the track.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 8.8 / 10 while the full run is pending.
- Evidence: the bounded limit-5 Colab PEFT route scored successfully across all
  selected tasks.
- Gaps: no-limit full task execution is pending and may hit Colab wall-clock or
  session stability limits.
- Decision: execute on Colab first; preserve all raw artifacts under the SSD
  eval root.
