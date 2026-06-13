# Plan: Qwen3 V4 PEFT Kaggle Scorecard

## Phase 1 - Kernel Spec

- [x] Task: Add a Kaggle runner for the public PEFT adapter scorecard.
- [x] Task: Add a guarded submitter that dry-runs by default.
- [x] Task: Stage `kernel-metadata.json`, run config, and runner code.
- [x] Task: Capture the dry-run command and artifact report.

## Phase 2 - Execute

- [x] Task: Verify the local Kaggle CLI is installed.
- [x] Task: Record the live Kaggle authentication blocker.
- [ ] Task: Authenticate the Kaggle CLI and check GPU quota.
- [ ] Task: Submit the no-limit kernel only after explicit confirmation.
- [ ] Task: Download result artifacts and update benchmark coverage if complete.

## Health Check

- Target: >= 9.0 / 10
- Current estimate: 8.8 / 10 as a prepared-but-blocked backend track.
- Evidence: `scripts/submit_kaggle_peft_scorecard.py` generated
  `reports/cloud/qwen3-v4-peft-kaggle-submit-dry-run-20260613.json` and staged
  the kernel folder under `reports/cloud/kaggle-qwen3-v4-peft-scorecard-20260613`.
- Gaps: Kaggle CLI is installed but unauthenticated, so quota and kernel push
  behavior are not yet live-tested.
- Decision: keep Kaggle prepared but blocked until authentication and quota are
  confirmed.
