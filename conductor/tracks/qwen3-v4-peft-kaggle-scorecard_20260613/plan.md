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
- [x] Task: Resolve Kaggle quota visibility.
- [x] Task: Confirm public-input notebook execution contract.
- [ ] Task: Submit the no-limit kernel only after explicit confirmation.
- [ ] Task: Download result artifacts and update benchmark coverage if complete.

## Health Check

- Target: >= 9.0 / 10
- Current estimate: 9.4 / 10 as a prepared-but-execution-gated backend track.
- Evidence: `scripts/submit_kaggle_peft_scorecard.py` generated
  `reports/cloud/qwen3-v4-peft-kaggle-submit-dry-run-20260613.json` and staged
  the kernel folder under `reports/cloud/kaggle-qwen3-v4-peft-scorecard-20260613`.
  The 2026-06-13 browser-assisted OAuth flow completed and the CLI reports the
  local account as `edithatogo`; the guarded submitter dry-run now records no
  auth blocker. The public `kaggle quota` command still has a renderer/parser
  failure, but the same authenticated SDK endpoint returned GPU quota
  `108000s` total / `0s` used and TPU quota `72000s` total / `0s` used, with
  refresh at `2026-06-20T00:00:00Z`. The staged notebook contract passed in
  `reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.md`: public inputs
  only, no private data upload, GPU script metadata, no `--limit`, 21600s
  timeout, and explicit `--execute --confirm-kaggle-run` operator boundary.
- Gaps: Kernel push/run behavior and result artifact recovery are not yet
  live-tested.
- Decision: keep Kaggle prepared but blocked until the no-limit kernel has
  explicit run approval.
