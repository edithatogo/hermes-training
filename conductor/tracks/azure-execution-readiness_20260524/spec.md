# Specification: Azure Scale-Out Execution Readiness

## Overview

Prepare the Azure lane for controlled benchmark, teacher, and evaluator execution without creating Azure resources during this track setup. The work should turn the existing Azure preflight and template lane into a fail-closed execution checklist that can be followed only after quota, account, region, workspace, compute, cost, and artifact-sync evidence are available.

## Requirements

- Confirm the active Azure account, subscription, region, Azure ML CLI extension, and GPU quota before any Azure ML workspace, compute, endpoint, or job resource is created.
- Treat quota confirmation as the first hard gate. Azure ML workspace and compute creation steps must remain blocked until the selected region and GPU family have sufficient quota.
- Preserve no-spend and fail-closed behavior: no paid resources, no persistent compute, no non-Spot GPU jobs, and no job submission when account, quota, budget, output path, or publication checks are missing.
- Require all cloud manifests and commands to use SSD-backed local paths for inputs, logs, downloaded reports, run cards, and synced outputs under `/Volumes/PortableSSD`.
- Add an execution checklist for Azure ML workspace and compute creation that is explicit, ordered, and conditional on quota approval.
- Define benchmark job dry-runs that validate command generation, environment variables, output paths, and fail-closed behavior before any live cloud run.
- Define teacher/evaluator run readiness for frontier model judging, dataset review, and benchmark comparison without widening scope into training sweeps.
- Require cloud outputs to be synced back to `/Volumes/PortableSSD` before repository docs, scorecards, or publication evidence are updated.
- Require publication evidence to include account/subscription proof, quota proof, cost guardrail proof, job manifest, run logs, result artifacts, sync location, benchmark summary, and explicit publication decision.

## Acceptance Criteria

- A Conductor track exists for Azure execution readiness with spec, plan, metadata, and index files.
- The track plan separates quota confirmation, fail-closed/no-spend checks, workspace/compute readiness, benchmark dry-runs, teacher/evaluator runs, SSD sync, and publication evidence.
- The plan contains no completed tasks and does not instruct the agent to create Azure resources during track setup.
- The registry links to the new track.

## Out Of Scope

- Creating Azure ML workspaces, compute clusters, storage accounts, registries, endpoints, or submitted jobs as part of this setup.
- Running paid Azure workloads before quota, budget, region, and fail-closed evidence pass.
- Publishing model artifacts, adapters, benchmark claims, or Hugging Face updates without synced evidence and an explicit publication decision.
- Broad training sweeps or exploratory cloud experiments unrelated to benchmark, teacher, and evaluator readiness.
