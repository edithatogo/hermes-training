# Plan: Qwen3 v4 PEFT Lightning Scorecard

## Phase 1 - Guarded Submitter

- [x] Task: Add `scripts/submit_lightning_peft_scorecard.py`.
- [x] Task: Stage `reports/cloud/lightning-qwen3-v4-peft-scorecard-20260614/lightning-peft-lm-eval-config.json`.
- [x] Task: Generate `reports/cloud/qwen3-v4-peft-lightning-submit-dry-run-20260614.json`.
- [x] Task: Add unit tests for command construction, config staging, confirmation gates, and Teamspace blockers.

## Phase 2 - Reporting

- [x] Task: Add Lightning submitter commands to the cloud unblock checklist.
- [x] Task: Add the Lightning scorecard track to the active blocked-track matrix.
- [ ] Task: Run Lightning login and identify a real Teamspace only after explicit user approval.
- [ ] Task: Confirm free credit/grant or zero-cost GPU policy.
- [ ] Task: Submit the no-limit job only after explicit approval.
- [ ] Task: Recover result artifacts to the SSD and run benchmark ingest validation.

## Health Check

- Target: >= 9.0 / 10
- Current estimate: 8.9 / 10 as a prepared-but-auth/teamspace/cost-gated backend track.
- Evidence:
  - Submitter and tests are present.
  - Dry-run report records `execute=false`, placeholder Teamspace, and no remote launch.
  - Cloud reports include guarded Lightning commands.
- Gaps: Lightning login/teamspace, machine policy, free credit/grant, and artifact recovery are not proven.
- Decision: Keep Lightning blocked until account and cost gates are explicitly cleared.
