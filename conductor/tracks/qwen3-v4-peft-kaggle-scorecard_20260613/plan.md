# Plan: Qwen3 V4 PEFT Kaggle Scorecard

## Phase 1 - Kernel Spec

- [x] Task: Add a Kaggle runner for the public PEFT adapter scorecard.
- [x] Task: Add a guarded submitter that dry-runs by default.
- [x] Task: Stage `kernel-metadata.json`, run config, and runner code.
- [x] Task: Capture the dry-run command and artifact report.

## Phase 2 - Execute

- [x] Task: Verify the local Kaggle CLI is installed.
- [x] Task: Record the live Kaggle authentication blocker.
- [x] Task: Authenticate the Kaggle CLI.
- [ ] Task: Resolve Kaggle quota visibility and confirm dataset terms.
- [ ] Task: Submit the no-limit kernel only after explicit confirmation.
- [ ] Task: Download result artifacts and update benchmark coverage if complete.

## Health Check

- Target: >= 9.0 / 10
- Current estimate: 8.9 / 10 as a prepared-but-quota-gated backend track.
- Evidence: `scripts/submit_kaggle_peft_scorecard.py` generated
  `reports/cloud/qwen3-v4-peft-kaggle-submit-dry-run-20260613.json` and staged
  the kernel folder under `reports/cloud/kaggle-qwen3-v4-peft-scorecard-20260613`.
  The 2026-06-13 browser-assisted OAuth flow completed and the CLI reports the
  local account as `edithatogo`; the guarded submitter dry-run now records no
  auth blocker.
- Gaps: `kaggle quota` currently fails with a CLI parsing error before returning
  weekly accelerator quota. Dataset terms and kernel push behavior are not yet
  live-tested.
- Decision: keep Kaggle prepared but blocked until quota visibility/terms are
  confirmed and the no-limit kernel has explicit run approval.
