# Hermes Shortlist Runtime and Promotion Execution Plan

## Phase 1: Evidence Baseline and Role Lock

- [ ] Task: Read `FUTURE_MODELS.md`, `MODEL_CANDIDATES.yaml`, `HANDOFF.md`, and the current scan report.
    - [ ] Confirm the exact Hermes candidates and their intended roles.
    - [ ] Separate local fine-tune targets, helper/extraction targets, and teacher/reference models.
    - [ ] Record any stale, duplicated, or contradictory candidate states before execution.
- [ ] Task: Run baseline validation before edits.
    - [ ] Run `source scripts/env.sh && ./.venv/bin/python scripts/validate_readiness.py`.
    - [ ] Run the model-candidate consistency check if candidate metadata changes are planned.
- [ ] Task: Conductor - User Manual Verification 'Evidence Baseline and Role Lock' (Protocol in workflow.md)

## Phase 2: Dynamic Runtime Execution

- [ ] Task: Prefer Colab CLI for heavy benchmark or smoke execution.
    - [ ] Confirm `colab sessions` and available runtime state.
    - [ ] Package the smallest reproducible job script for each offloaded benchmark.
    - [ ] Download only bounded result artifacts back into the repo.
- [ ] Task: Use Mac/Metal paths for local proof and parity.
    - [ ] Run MLX proof where a candidate has MLX packaging.
    - [ ] Run llama.cpp, Ollama, or LM Studio proof where GGUF or OpenAI-compatible runtime coverage exists.
- [ ] Task: Gate Azure and NVIDIA/NGC execution.
    - [ ] Run Azure login/quota/capacity preflight before any Azure job.
    - [ ] Run NGC API-key and container/model availability preflight before any NVIDIA job.
    - [ ] Stop before paid execution or restricted-license downloads unless approved.
- [ ] Task: Conductor - User Manual Verification 'Dynamic Runtime Execution' (Protocol in workflow.md)

## Phase 3: Benchmark and Promotion Gate

- [ ] Task: Execute strict Hermes benchmark slices.
    - [ ] Run standard benchmark coverage for each candidate where runtime proof exists.
    - [ ] Include strict tool-call, role, formatting, and local pilot gates.
    - [ ] Capture failures as first-class evidence rather than retrying without explanation.
- [ ] Task: Make promotion decisions.
    - [ ] Promote only candidates that pass runtime, benchmark, and format gates.
    - [ ] Keep helper candidates separate from main Hermes runtime candidates.
    - [ ] Record rejected or blocked candidates with concrete blocker text.
- [ ] Task: Conductor - User Manual Verification 'Benchmark and Promotion Gate' (Protocol in workflow.md)

## Phase 4: Documentation and Registry Reconciliation

- [ ] Task: Update roadmap and candidate artifacts.
    - [ ] Update `FUTURE_MODELS.md`.
    - [ ] Update `MODEL_CANDIDATES.yaml`.
    - [ ] Update relevant benchmark reports and runtime proof queues.
- [ ] Task: Validate and checkpoint.
    - [ ] Rerun readiness and candidate consistency checks.
    - [ ] Update track status and summarize remaining blockers.
    - [ ] Commit and push only reproducible, non-secret artifacts.
- [ ] Task: Conductor - User Manual Verification 'Documentation and Registry Reconciliation' (Protocol in workflow.md)
