# Plan: Qwen3 v4 PEFT Lightning Scorecard

## Phase 1 - Guarded Submitter

- [x] Task: Add `scripts/submit_lightning_peft_scorecard.py`.
- [x] Task: Stage `reports/cloud/lightning-qwen3-v4-peft-scorecard-20260614/lightning-peft-lm-eval-config.json`.
- [x] Task: Generate `reports/cloud/qwen3-v4-peft-lightning-submit-dry-run-20260614.json`.
- [x] Task: Add unit tests for command construction, config staging, confirmation gates, and Teamspace blockers.

## Phase 2 - Reporting

- [x] Task: Add Lightning submitter commands to the cloud unblock checklist.
- [x] Task: Add the Lightning scorecard track to the active blocked-track matrix.
- [x] Task: Defer Lightning login and Teamspace selection until the user
  explicitly chooses Lightning execution.
- [x] Task: Defer free credit/grant or zero-cost GPU policy confirmation until
  Lightning is selected for cross-provider comparison.
- [x] Task: Defer no-limit Lightning submission; keep execution guarded behind
  explicit approval.
- [x] Task: Defer Lightning result artifact recovery; use Kaggle v7 artifacts
  for current benchmark coverage.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10 as a prepared/deferred backend track with current
  benchmark coverage supplied by Kaggle v7.
- Evidence:
  - Submitter and tests are present.
  - Dry-run report records `execute=false`, placeholder Teamspace, and no remote launch.
  - Cloud reports include guarded Lightning commands.
- Gaps: Lightning login/teamspace, machine policy, free credit/grant, and
  artifact recovery are not proven. This is no longer a blocker for the current
  selected-task scorecard because Kaggle kernel version 7 completed all five
  no-limit tasks and passed the no-pending ingest gate.
- Decision: close Lightning as a guarded fallback. Do not run Lightning login
  or submit jobs unless the user explicitly chooses Lightning for
  cross-provider comparison and confirms account/cost gates.
