# Cross-Runtime Proof Matrix Execution Plan

## Phase 1: Runtime Inventory and Candidate Mapping

- [ ] Task: Build the candidate-to-runtime matrix.
    - [ ] Read active candidates from `MODEL_CANDIDATES.yaml`.
    - [ ] Map each candidate to MLX, GGUF, Ollama, LM Studio, Transformers, ONNX/CoreML, Colab, Azure, and NGC feasibility.
    - [ ] Mark required licenses, artifacts, and expected hardware limits.
- [ ] Task: Identify duplicate or obsolete runtime proof entries.
    - [ ] Reconcile proof queues against completed scan report.
    - [ ] Preserve historical evidence while marking stale lanes clearly.
- [ ] Task: Conductor - User Manual Verification 'Runtime Inventory and Candidate Mapping' (Protocol in workflow.md)

## Phase 2: Local Mac/Metal Runtime Proofs

- [ ] Task: Execute Mac/Metal first where feasible.
    - [ ] Run MLX proof for MLX-packaged candidates.
    - [ ] Run llama.cpp proof for GGUF-packaged candidates.
    - [ ] Run Ollama or LM Studio proof where operational packaging is relevant.
- [ ] Task: Capture strict runtime observations.
    - [ ] Record load success, prompt format, output shape, latency, memory pressure, and failure mode.
    - [ ] Avoid long local runs when a Colab offload path is available and adequate.
- [ ] Task: Conductor - User Manual Verification 'Local Mac/Metal Runtime Proofs' (Protocol in workflow.md)

## Phase 3: Cloud and Dynamic Backend Proofs

- [ ] Task: Use Colab CLI for bounded dynamic jobs.
    - [ ] Create session or fresh-run scripts for benchmark slices.
    - [ ] Upload sanitized inputs only.
    - [ ] Download result summaries and release sessions.
- [ ] Task: Gate Azure execution.
    - [ ] Run `az account show` and login if required.
    - [ ] Confirm subscription, region, quota, and cost boundary before GPU work.
- [ ] Task: Gate NVIDIA/NGC execution.
    - [ ] Run `ngc config current`.
    - [ ] Confirm API key, org/team, entitlements, and container/model availability before use.
- [ ] Task: Conductor - User Manual Verification 'Cloud and Dynamic Backend Proofs' (Protocol in workflow.md)

## Phase 4: Documentation and Reproducibility

- [ ] Task: Update runtime proof artifacts.
    - [ ] Update proof queues and benchmark reports.
    - [ ] Update `MODEL_CANDIDATES.yaml` runtime fields.
    - [ ] Update `FUTURE_MODELS.md` only for roadmap-level decisions.
- [ ] Task: Validate and checkpoint.
    - [ ] Run readiness and candidate checks.
    - [ ] Commit and push bounded evidence and docs.
- [ ] Task: Conductor - User Manual Verification 'Documentation and Reproducibility' (Protocol in workflow.md)
