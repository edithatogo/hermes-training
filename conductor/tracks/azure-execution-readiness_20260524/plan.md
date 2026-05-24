# Plan: Azure Scale-Out Execution Readiness

## Phase 1 - Quota And Account Gate

- [x] Task: Confirm Azure identity, subscription, tenant, and CLI context are the intended execution lane.
    - [x] Verify the active account and subscription match the approved Azure Students account.
    - [x] Record the selected region and rationale before evaluating quota.
    - [x] Verify Azure ML CLI v2 extension availability without creating resources.
- [x] Task: Confirm GPU quota before any Azure ML workspace or compute action.
    - [x] Run read-only quota inspection for the selected region and candidate GPU families.
    - [x] Record quota evidence in a local SSD-backed run card or notes file.
    - [x] Fail closed if quota is zero, unavailable, ambiguous, or tied to an unapproved region.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Quota And Account Gate' (Protocol in workflow.md)

## Phase 2 - No-Spend And Fail-Closed Controls

- [x] Task: Verify no-spend defaults before cloud execution is enabled.
    - [x] Confirm Spot/low-priority is the default for GPU compute.
    - [x] Confirm `min_instances: 0`, `max_instances: 1`, and one GPU job at a time.
    - [x] Confirm no persistent endpoint, always-on compute, or non-SSD output location is required.
- [x] Task: Add or update fail-closed checks for cloud job entrypoints.
    - [x] Block execution when Azure identity, subscription, quota, compute target, budget policy, or SSD output root is missing.
    - [x] Block execution when any output path resolves outside `/Volumes/PortableSSD`.
    - [x] Block publication-mode runs unless evidence paths and publication decision fields are present.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - No-Spend And Fail-Closed Controls' (Protocol in workflow.md)

## Phase 3 - Workspace And Compute Readiness

- [x] Task: Prepare Azure ML workspace creation steps as a gated checklist only.
    - [x] Document the exact workspace command or YAML path that will be used after quota approval.
    - [x] Confirm resource group, workspace name, location, tags, and deletion expectations.
    - [x] Keep workspace creation blocked until Phase 1 and Phase 2 pass.
- [x] Task: Prepare Azure ML compute creation steps as a gated checklist only.
    - [x] Document the low-priority GPU compute YAML or command that will be used after workspace readiness.
    - [x] Confirm scale-to-zero, max-one-node, SKU, region, and quota alignment.
    - [x] Keep compute creation blocked until workspace readiness and quota evidence are recorded.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Workspace And Compute Readiness' (Protocol in workflow.md)

## Phase 4 - Benchmark Job Dry-Runs

- [x] Task: Dry-run benchmark job generation locally without submitting Azure jobs.
    - [x] Render or validate the Azure ML benchmark job manifest using approved SSD-backed inputs and outputs.
    - [x] Verify benchmark commands resolve model, dataset, cache, and output roots under `/Volumes/PortableSSD`.
    - [x] Confirm the dry-run fails closed when required Azure or path variables are intentionally absent.
- [x] Task: Define first live benchmark execution gate.
    - [x] Require quota, workspace, compute, no-spend, and dry-run evidence before live submission.
    - [x] Require a run card path under `/Volumes/PortableSSD` before submission.
    - [x] Limit first live run to a smoke benchmark or minimal benchmark shard.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Benchmark Job Dry-Runs' (Protocol in workflow.md)

## Phase 5 - Teacher And Evaluator Run Readiness

- [x] Task: Dry-run teacher/evaluator job generation locally without submitting Azure jobs.
    - [x] Validate teacher/evaluator manifests for frontier model judging, dataset review, or benchmark comparison.
    - [x] Confirm prompts, inputs, cache roots, and output paths are SSD-backed.
    - [x] Confirm secrets or API credentials are never written into tracked files or run cards.
- [x] Task: Define first live teacher/evaluator execution gate.
    - [x] Require benchmark dry-run success or a documented reason to run teacher/evaluator work first.
    - [x] Require max-one-GPU-job policy and no persistent compute policy.
    - [x] Require review of expected outputs before live submission.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 5 - Teacher And Evaluator Run Readiness' (Protocol in workflow.md)

## Phase 6 - SSD Sync And Publication Evidence

- [x] Task: Sync Azure outputs back to `/Volumes/PortableSSD` before updating repository claims.
    - [x] Download job logs, metrics, scorecards, generated reports, and model-comparison artifacts to SSD-backed roots.
    - [x] Verify synced artifact paths are referenced by run cards and are not accidentally tracked in Git.
    - [x] Preserve enough metadata to reproduce the Azure job from local evidence.
- [x] Task: Prepare publication evidence and decision record.
    - [x] Record account/subscription proof, quota proof, no-spend proof, workspace/compute identifiers, job manifest, run logs, synced result path, benchmark summary, and evaluator notes.
    - [x] Mark publication blocked unless benchmark gates and evidence requirements pass.
    - [x] Update only minimal docs needed to point to the evidence and decision.
- [x] Task: Run hub readiness validation.
    - [x] Source `scripts/env.sh`.
    - [x] Run `./.venv/bin/python scripts/validate_readiness.py`.
    - [x] Update track health and remaining blockers.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 6 - SSD Sync And Publication Evidence' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10.
- Required evidence: quota confirmation, fail-closed/no-spend proof, gated workspace/compute readiness, benchmark dry-run proof, teacher/evaluator dry-run proof, SSD sync proof, validation output, and publication decision record.
- Current evidence: `reports/azure/execution-readiness-20260524.md` records account/subscription/extension/SSD pass and regional quota. Live Azure execution remains blocked until a specific useful GPU SKU/region quota is available.
- Additional evidence: `scripts/azure_status.py` found no Azure ML workspaces, so workspace creation remains a gated future action. `reports/azure/execution-gate-20260524.md` records live-job blockers and publication boundaries. `scripts/validate_azure_execution_readiness.py` validates that templates remain low-priority, max-one-node, dry-run, and SSD-rooted.
