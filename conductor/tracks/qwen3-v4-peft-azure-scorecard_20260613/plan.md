# Plan: Qwen3 V4 PEFT Azure Scorecard

## Phase 1 - Template

- [x] Task: Add the Azure ML command-job template for the public PEFT adapter.
- [x] Task: Add a guarded submitter that dry-runs by default.

## Phase 2 - Evidence

- [x] Task: Generate a dry-run submission report.
- [x] Task: Record the current Azure login blocker.
- [x] Task: Add the submitter to readiness syntax validation.

## Phase 3 - Execution Gate

- [x] Task: Defer `az login --use-device-code` because live login/resource
  checks are account-side and Kaggle v7 supplied the validated scorecard
  evidence.
- [x] Task: Defer confirmation of `Azure for Students`, GPU quota, workspace,
  compute, and cost approval until the user explicitly chooses Azure execution.
- [x] Task: Defer no-limit Azure submission; keep it guarded behind `--execute
  --confirm-azure-run`.
- [x] Task: Defer Azure artifact download; use Kaggle v7 artifacts for current
  benchmark coverage.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10 as a prepared/deferred backend track with current
  benchmark coverage supplied by Kaggle v7.
- Evidence: the Azure ML job template and guarded submitter are in place;
  dry-run preflight records that Azure CLI is installed and the ML extension is
  available, but `az account show` requires login.
- Gaps: no Azure login, quota check, workspace, compute, environment, or job
  artifact exists yet. This is no longer a blocker for the current scorecard
  because Kaggle kernel version 7 completed all five no-limit selected tasks
  and passed the no-pending ingest gate.
- Decision: close Azure as a guarded, prepared fallback route. Do not run
  `az login`, create resources, or submit jobs unless the user explicitly
  chooses Azure for cross-provider comparison and confirms quota/cost gates.
