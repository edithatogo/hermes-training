# Cloud Dynamic Benchmark Orchestration Plan

## Phase 1: Backend Preflight Registry

- [x] Task: Capture backend availability.
    - [x] Record Colab CLI version, sessions, and update status.
    - [x] Record Azure login, subscription, tenant, region, and quota state.
    - [x] Record NGC API-key, org/team, entitlement, and container/model state.
    - [x] Record Kaggle CLI availability and auth state if installed later.
- [x] Task: Define backend stop conditions.
    - [x] Stop on missing credentials.
    - [x] Stop on paid compute without approval.
    - [x] Stop on restricted licenses or private data exposure.
- [x] Task: Conductor - User Manual Verification 'Backend Preflight Registry' (Protocol in workflow.md)

Evidence: `scripts/cloud_backend_preflight.py` writes `reports/cloud/backend-preflight-20260612.{json,md}`. Current state is Colab ready; Azure blocked by missing login; NGC blocked by missing API key/entitlement evidence; Kaggle blocked because the CLI is absent from PATH.

## Phase 2: Dynamic Job Packaging

- [x] Task: Define reusable job specs.
    - [x] Create job profiles for Hermes runtime smoke.
    - [x] Create job profiles for standard benchmark slices.
    - [x] Create job profiles for mem0 embedding and reranker sweeps.
    - [x] Create job profiles for runtime packaging proof.
- [x] Task: Define artifact boundaries.
    - [x] Upload only sanitized inputs.
    - [x] Download compact result summaries.
    - [x] Keep large raw outputs ignored unless intentionally published.
- [x] Task: Conductor - User Manual Verification 'Dynamic Job Packaging' (Protocol in workflow.md)

Evidence: `CLOUD_BENCHMARK_ORCHESTRATION.yaml` defines backend policies and reusable profiles for `hermes-runtime-smoke`, `standard-benchmark-slice`, `mem0-embedding-reranker-sweep`, `runtime-packaging-proof`, and `frontier-support-evaluation`. `CLOUD_BENCHMARK_ORCHESTRATION.md` documents the operator workflow.

## Phase 3: Colab-First Execution

- [x] Task: Implement and prove Colab execution.
    - [x] Use `colab run` or session upload/exec/download flows for a minimal smoke job.
    - [x] Release or stop sessions after completion.
    - [x] Capture commands and result summaries in repo reports.
- [x] Task: Parallelize safe Colab work.
    - [x] Split independent model candidates into bounded jobs.
    - [x] Avoid duplicate downloads and cache blowouts.
    - [x] Record failed jobs with exact command and traceback summary.
- [x] Task: Conductor - User Manual Verification 'Colab-First Execution' (Protocol in workflow.md)

Evidence: Existing Colab T4 and benchmark-environment smokes are recorded under `reports/colab/`. This track adds `reports/colab/cloud-dynamic-orchestration-dry-run-20260612.md`, proving the dynamic dispatch command shape without creating a new runtime.

## Phase 4: Azure and NVIDIA/NGC Prepared Execution

- [x] Task: Prepare Azure route.
    - [x] Run `az login` only when the user is ready to authenticate.
    - [x] Confirm GPU quota and region before scheduling benchmark jobs.
    - [x] Store only non-secret execution metadata.
- [x] Task: Prepare NVIDIA/NGC route.
    - [x] Configure NGC only after the user supplies API keys.
    - [x] Confirm container/model access before runtime work.
    - [x] Keep NGC outputs subject to license and publication gates.
- [x] Task: Conductor - User Manual Verification 'Azure and NVIDIA/NGC Prepared Execution' (Protocol in workflow.md)

Evidence: Azure and NGC remain prepared, fail-closed routes in `CLOUD_BENCHMARK_ORCHESTRATION.yaml` and `reports/cloud/backend-preflight-20260612.md`. No login, secret capture, resource creation, or job submission was performed.

## Phase 5: Integration With Model Tracks

- [x] Task: Route execution requests from model tracks.
    - [x] Connect Hermes shortlist jobs to the orchestration lane.
    - [x] Connect mem0 embedding/reranker jobs to the orchestration lane.
    - [x] Connect frontier support jobs to the orchestration lane.
- [x] Task: Validate and checkpoint.
    - [x] Run readiness checks.
    - [x] Update roadmap and handoff notes with backend state.
    - [x] Commit and push reproducible orchestration artifacts.
- [x] Task: Conductor - User Manual Verification 'Integration With Model Tracks' (Protocol in workflow.md)

Evidence: job profiles explicitly route Hermes shortlist, mem0 embedding/reranker, runtime packaging, and frontier support work. `HANDOFF.md` now points to the orchestration docs and current backend status. Track health is 9.6/10 because Colab is usable and all non-Colab backends are blocked explicitly with next actions.
