# Plan: LFM2.5 Full-Smoke-Data Training and Evaluation

## Phase 1: Preparation

- [x] Task: Audit current dataset tokens and truncation risk.
- [x] Task: Create full-smoke-data LFM2.5 training config.
- [x] Task: Dry-run config and validate readiness.
- [x] Task: Conductor - Automated Review and Checkpoint 'Preparation' (Protocol in workflow.md)

## Phase 2: Training

- [x] Task: Run full-smoke-data training with SSD-backed env.
- [x] Task: Capture trained tokens, loss, peak memory, elapsed time.
- [x] Task: Save adapter and run note.
- [x] Task: Conductor - Automated Review and Checkpoint 'Training' (Protocol in workflow.md)

## Phase 3: Evaluation

- [x] Task: Run base model evaluation.
- [x] Task: Run adapter evaluation.
- [x] Task: Generate comparison report.
- [x] Task: Update docs with result and next decision.
- [x] Task: Conductor - Automated Review and Checkpoint 'Evaluation' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: dataset audit confirmed at 461 train rows / 219,354 tokens; config dry-run passed offline; full-smoke training completed for 200 iterations / 175,895 trained tokens with final validation loss 1.455, peak memory 6.022 GB, and elapsed time 334.3 seconds; base and adapter evaluation completed on 100 prompts; summary recorded in `lfm2/eval/lfm25-full-smoke-summary.md`.
- Decision: adapter loading and evaluation are proven, but this adapter is not publishable because it collapses to empty or near-empty responses. The next recipe should lower learning rate and add an early response-length gate before scaling.
- Gaps: follow-up training recipe remains outside this completed proof track.
- [x] Task: Estimate track health using hub `conductor/health-score.md`.
- [x] Task: Close or document all gaps below health 9.5.
- [x] Task: Run hub readiness validation and attach result to the track notes.
- [x] Task: Confirm health >= 9.5 before marking this track complete.
