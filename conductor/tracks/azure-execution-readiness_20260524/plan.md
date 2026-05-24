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
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Quota And Account Gate' (Protocol in workflow.md)

## Phase 2 - No-Spend And Fail-Closed Controls

- [ ] Task: Verify no-spend defaults before cloud execution is enabled.
    - [ ] Confirm Spot/low-priority is the default for GPU compute.
    - [ ] Confirm `min_instances: 0`, `max_instances: 1`, and one GPU job at a time.
    - [ ] Confirm no persistent endpoint, always-on compute, or non-SSD output location is required.
- [ ] Task: Add or update fail-closed checks for cloud job entrypoints.
    - [ ] Block execution when Azure identity, subscription, quota, compute target, budget policy, or SSD output root is missing.
    - [ ] Block execution when any output path resolves outside `/Volumes/PortableSSD`.
    - [ ] Block publication-mode runs unless evidence paths and publication decision fields are present.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - No-Spend And Fail-Closed Controls' (Protocol in workflow.md)

## Phase 3 - Workspace And Compute Readiness

- [ ] Task: Prepare Azure ML workspace creation steps as a gated checklist only.
    - [ ] Document the exact workspace command or YAML path that will be used after quota approval.
    - [ ] Confirm resource group, workspace name, location, tags, and deletion expectations.
    - [ ] Keep workspace creation blocked until Phase 1 and Phase 2 pass.
- [ ] Task: Prepare Azure ML compute creation steps as a gated checklist only.
    - [ ] Document the low-priority GPU compute YAML or command that will be used after workspace readiness.
    - [ ] Confirm scale-to-zero, max-one-node, SKU, region, and quota alignment.
    - [ ] Keep compute creation blocked until workspace readiness and quota evidence are recorded.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Workspace And Compute Readiness' (Protocol in workflow.md)

## Phase 4 - Benchmark Job Dry-Runs

- [ ] Task: Dry-run benchmark job generation locally without submitting Azure jobs.
    - [ ] Render or validate the Azure ML benchmark job manifest using approved SSD-backed inputs and outputs.
    - [ ] Verify benchmark commands resolve model, dataset, cache, and output roots under `/Volumes/PortableSSD`.
    - [ ] Confirm the dry-run fails closed when required Azure or path variables are intentionally absent.
- [ ] Task: Define first live benchmark execution gate.
    - [ ] Require quota, workspace, compute, no-spend, and dry-run evidence before live submission.
    - [ ] Require a run card path under `/Volumes/PortableSSD` before submission.
    - [ ] Limit first live run to a smoke benchmark or minimal benchmark shard.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Benchmark Job Dry-Runs' (Protocol in workflow.md)

## Phase 5 - Teacher And Evaluator Run Readiness

- [ ] Task: Dry-run teacher/evaluator job generation locally without submitting Azure jobs.
    - [ ] Validate teacher/evaluator manifests for frontier model judging, dataset review, or benchmark comparison.
    - [ ] Confirm prompts, inputs, cache roots, and output paths are SSD-backed.
    - [ ] Confirm secrets or API credentials are never written into tracked files or run cards.
- [ ] Task: Define first live teacher/evaluator execution gate.
    - [ ] Require benchmark dry-run success or a documented reason to run teacher/evaluator work first.
    - [ ] Require max-one-GPU-job policy and no persistent compute policy.
    - [ ] Require review of expected outputs before live submission.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 5 - Teacher And Evaluator Run Readiness' (Protocol in workflow.md)

## Phase 6 - SSD Sync And Publication Evidence

- [ ] Task: Sync Azure outputs back to `/Volumes/PortableSSD` before updating repository claims.
    - [ ] Download job logs, metrics, scorecards, generated reports, and model-comparison artifacts to SSD-backed roots.
    - [ ] Verify synced artifact paths are referenced by run cards and are not accidentally tracked in Git.
    - [ ] Preserve enough metadata to reproduce the Azure job from local evidence.
- [ ] Task: Prepare publication evidence and decision record.
    - [ ] Record account/subscription proof, quota proof, no-spend proof, workspace/compute identifiers, job manifest, run logs, synced result path, benchmark summary, and evaluator notes.
    - [ ] Mark publication blocked unless benchmark gates and evidence requirements pass.
    - [ ] Update only minimal docs needed to point to the evidence and decision.
- [ ] Task: Run hub readiness validation.
    - [ ] Source `scripts/env.sh`.
    - [ ] Run `./.venv/bin/python scripts/validate_readiness.py`.
    - [ ] Update track health and remaining blockers.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 6 - SSD Sync And Publication Evidence' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.0 / 10.
- Required evidence: quota confirmation, fail-closed/no-spend proof, gated workspace/compute readiness, benchmark dry-run proof, teacher/evaluator dry-run proof, SSD sync proof, validation output, and publication decision record.
- Current evidence: `reports/azure/execution-readiness-20260524.md` records account/subscription/extension/SSD pass and regional quota. Live Azure execution remains blocked until a specific useful GPU SKU/region quota is available.
