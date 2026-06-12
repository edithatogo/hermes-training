# Cloud Dynamic Benchmark Orchestration Plan

## Phase 1: Backend Preflight Registry

- [ ] Task: Capture backend availability.
    - [ ] Record Colab CLI version, sessions, and update status.
    - [ ] Record Azure login, subscription, tenant, region, and quota state.
    - [ ] Record NGC API-key, org/team, entitlement, and container/model state.
    - [ ] Record Kaggle CLI availability and auth state if installed later.
- [ ] Task: Define backend stop conditions.
    - [ ] Stop on missing credentials.
    - [ ] Stop on paid compute without approval.
    - [ ] Stop on restricted licenses or private data exposure.
- [ ] Task: Conductor - User Manual Verification 'Backend Preflight Registry' (Protocol in workflow.md)

## Phase 2: Dynamic Job Packaging

- [ ] Task: Define reusable job specs.
    - [ ] Create job profiles for Hermes runtime smoke.
    - [ ] Create job profiles for standard benchmark slices.
    - [ ] Create job profiles for mem0 embedding and reranker sweeps.
    - [ ] Create job profiles for runtime packaging proof.
- [ ] Task: Define artifact boundaries.
    - [ ] Upload only sanitized inputs.
    - [ ] Download compact result summaries.
    - [ ] Keep large raw outputs ignored unless intentionally published.
- [ ] Task: Conductor - User Manual Verification 'Dynamic Job Packaging' (Protocol in workflow.md)

## Phase 3: Colab-First Execution

- [ ] Task: Implement and prove Colab execution.
    - [ ] Use `colab run` or session upload/exec/download flows for a minimal smoke job.
    - [ ] Release or stop sessions after completion.
    - [ ] Capture commands and result summaries in repo reports.
- [ ] Task: Parallelize safe Colab work.
    - [ ] Split independent model candidates into bounded jobs.
    - [ ] Avoid duplicate downloads and cache blowouts.
    - [ ] Record failed jobs with exact command and traceback summary.
- [ ] Task: Conductor - User Manual Verification 'Colab-First Execution' (Protocol in workflow.md)

## Phase 4: Azure and NVIDIA/NGC Prepared Execution

- [ ] Task: Prepare Azure route.
    - [ ] Run `az login` only when the user is ready to authenticate.
    - [ ] Confirm GPU quota and region before scheduling benchmark jobs.
    - [ ] Store only non-secret execution metadata.
- [ ] Task: Prepare NVIDIA/NGC route.
    - [ ] Configure NGC only after the user supplies API keys.
    - [ ] Confirm container/model access before runtime work.
    - [ ] Keep NGC outputs subject to license and publication gates.
- [ ] Task: Conductor - User Manual Verification 'Azure and NVIDIA/NGC Prepared Execution' (Protocol in workflow.md)

## Phase 5: Integration With Model Tracks

- [ ] Task: Route execution requests from model tracks.
    - [ ] Connect Hermes shortlist jobs to the orchestration lane.
    - [ ] Connect mem0 embedding/reranker jobs to the orchestration lane.
    - [ ] Connect frontier support jobs to the orchestration lane.
- [ ] Task: Validate and checkpoint.
    - [ ] Run readiness checks.
    - [ ] Update roadmap and handoff notes with backend state.
    - [ ] Commit and push reproducible orchestration artifacts.
- [ ] Task: Conductor - User Manual Verification 'Integration With Model Tracks' (Protocol in workflow.md)
