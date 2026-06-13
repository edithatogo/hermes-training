# Plan: Qwen3 V4 PEFT Azure Scorecard

## Phase 1 - Template

- [x] Task: Add the Azure ML command-job template for the public PEFT adapter.
- [x] Task: Add a guarded submitter that dry-runs by default.

## Phase 2 - Evidence

- [x] Task: Generate a dry-run submission report.
- [x] Task: Record the current Azure login blocker.
- [x] Task: Add the submitter to readiness syntax validation.

## Phase 3 - Execution Gate

- [ ] Task: Complete `az login --use-device-code` for the student account.
- [ ] Task: Confirm `Azure for Students`, GPU quota, workspace, compute, and
  cost approval.
- [ ] Task: Submit the no-limit scorecard only with `--execute
  --confirm-azure-run`.
- [ ] Task: Download Azure artifacts to `/Volumes/PortableSSD` and update
  benchmark coverage if complete.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.5 / 10 as a prepared-but-blocked backend track.
- Evidence: the Azure ML job template and guarded submitter are in place;
  dry-run preflight records that Azure CLI is installed and the ML extension is
  available, but `az account show` requires login.
- Gaps: no Azure login, quota check, workspace, compute, environment, or job
  artifact exists yet.
- Decision: keep Azure prepared but blocked until account-side login and quota
  gates pass.
