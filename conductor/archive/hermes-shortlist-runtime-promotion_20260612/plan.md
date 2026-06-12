# Hermes Shortlist Runtime and Promotion Execution Plan

## Phase 1: Evidence Baseline and Role Lock

- [x] Task: Read `FUTURE_MODELS.md`, `MODEL_CANDIDATES.yaml`, `HANDOFF.md`, and the current scan report.
    - [x] Confirm the exact Hermes candidates and their intended roles.
    - [x] Separate local fine-tune targets, helper/extraction targets, and teacher/reference models.
    - [x] Record any stale, duplicated, or contradictory candidate states before execution.
- [x] Task: Run baseline validation before edits.
    - [x] Run `source scripts/env.sh && ./.venv/bin/python scripts/validate_readiness.py`.
    - [x] Run the model-candidate consistency check if candidate metadata changes are planned.
- [x] Task: Conductor - User Manual Verification 'Evidence Baseline and Role Lock' (Protocol in workflow.md)

## Phase 2: Dynamic Runtime Execution

- [x] Task: Prefer Colab CLI for heavy benchmark or smoke execution.
    - [x] Confirm `colab sessions` and available runtime state.
    - [x] Package the smallest reproducible job script for each offloaded benchmark.
    - [x] Download only bounded result artifacts back into the repo.
- [x] Task: Use Mac/Metal paths for local proof and parity.
    - [x] Run MLX proof where a candidate has MLX packaging.
    - [x] Run llama.cpp, Ollama, or LM Studio proof where GGUF or OpenAI-compatible runtime coverage exists.
- [x] Task: Gate Azure and NVIDIA/NGC execution.
    - [x] Run Azure login/quota/capacity preflight before any Azure job.
    - [x] Run NGC API-key and container/model availability preflight before any NVIDIA job.
    - [x] Stop before paid execution or restricted-license downloads unless approved.
- [x] Task: Conductor - User Manual Verification 'Dynamic Runtime Execution' (Protocol in workflow.md)

## Phase 3: Benchmark and Promotion Gate

- [x] Task: Execute strict Hermes benchmark slices.
    - [x] Run standard benchmark coverage for each candidate where runtime proof exists.
    - [x] Include strict tool-call, role, formatting, and local pilot gates.
    - [x] Capture failures as first-class evidence rather than retrying without explanation.
    - Evidence: `reports/benchmark/local-pilots/tiny-helper-standard-benchmark-execution-20260612.md`, `reports/benchmark/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-pilots-20260525.md`, `reports/benchmark/official-ifeval/qwen3-4b-v4-targeted-ifeval-pilot-20260526.md`.
- [x] Task: Make promotion decisions.
    - [x] Promote only candidates that pass runtime, benchmark, and format gates.
    - [x] Keep helper candidates separate from main Hermes runtime candidates.
    - [x] Record rejected or blocked candidates with concrete blocker text.
    - Evidence: `MODEL_CANDIDATES.yaml`, `reports/benchmark/local-pilots/tiny-helper-standard-benchmark-execution-20260612.md`, `reports/runtime/hermes-shortlist-mac-metal-parity-20260612.md`.
- [x] Task: Conductor - User Manual Verification 'Benchmark and Promotion Gate' (Protocol in workflow.md)

## Phase 4: Documentation and Registry Reconciliation

- [x] Task: Update roadmap and candidate artifacts.
    - [x] Update `FUTURE_MODELS.md`.
    - [x] Update `MODEL_CANDIDATES.yaml`.
    - [x] Update relevant benchmark reports and runtime proof queues.
    - Evidence: `FUTURE_MODELS.md`, `MODEL_CANDIDATES.yaml`, `reports/runtime/cloud-gate-preflight-20260612.md`, `reports/runtime/hermes-shortlist-mac-metal-parity-20260612.md`.
- [x] Task: Validate and checkpoint.
    - [x] Rerun readiness and candidate consistency checks.
    - [x] Update track status and summarize remaining blockers.
    - [x] Commit and push only reproducible, non-secret artifacts.
- [x] Task: Conductor - User Manual Verification 'Documentation and Registry Reconciliation' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.5 / 10
- Evidence: SSD-first runtime and benchmark proofs are recorded, readiness and candidate consistency checks pass, the shortlist is separated into promoted runtime, helper/extraction, and blocked lanes, and direct MLX lm-eval official-pilot smokes now exist for Qwen3.5 0.8B and 2B.
- Gaps: broader official candidate coverage continues in separate follow-on tracks, but this track's required verification and promotion evidence is now closed.
- Decision: complete; archive the track after registry reconciliation.
