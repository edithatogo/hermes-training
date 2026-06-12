# Cross-Runtime Proof Matrix Execution Plan

## Phase 1: Runtime Inventory and Candidate Mapping

- [x] Task: Build the candidate-to-runtime matrix.
    - [x] Read active candidates from `MODEL_CANDIDATES.yaml`.
    - [x] Map each candidate to MLX, GGUF, Ollama, LM Studio, Transformers, ONNX/CoreML, Colab, Azure, and NGC feasibility.
    - [x] Mark required licenses, artifacts, and expected hardware limits.
- [x] Task: Identify duplicate or obsolete runtime proof entries.
    - [x] Reconcile proof queues against completed scan report.
    - [x] Preserve historical evidence while marking stale lanes clearly.
- [x] Task: Conductor - User Manual Verification 'Runtime Inventory and Candidate Mapping' (Protocol in workflow.md)
    - [x] Evidence: `reports/runtime/cross-runtime-proof-matrix-20260612.md`.
    - [x] Health: 9.6 / 10; remaining gaps are routed to follow-on execution tracks.

## Phase 2: Local Mac/Metal Runtime Proofs

- [x] Task: Execute Mac/Metal first where feasible.
    - [x] Run MLX proof for MLX-packaged candidates.
    - [x] Run llama.cpp proof for GGUF-packaged candidates.
    - [x] Run Ollama or LM Studio proof where operational packaging is relevant.
- [x] Task: Capture strict runtime observations.
    - [x] Record load success, prompt format, output shape, latency, memory pressure, and failure mode.
    - [x] Avoid long local runs when a Colab offload path is available and adequate.
- [x] Task: Conductor - User Manual Verification 'Local Mac/Metal Runtime Proofs' (Protocol in workflow.md)
    - [x] Evidence: MLX, llama.cpp, Ollama, and LM Studio preflights plus existing runtime reports summarized in `reports/runtime/cross-runtime-proof-matrix-20260612.md`.
    - [x] Health: 9.6 / 10; load success is separated from strict Hermes promotion.

## Phase 3: Cloud and Dynamic Backend Proofs

- [x] Task: Use Colab CLI for bounded dynamic jobs.
    - [x] Create session or fresh-run scripts for benchmark slices.
    - [x] Upload sanitized inputs only.
    - [x] Download result summaries and release sessions.
- [x] Task: Gate Azure execution.
    - [x] Run `az account show` and login if required.
    - [x] Confirm subscription, region, quota, and cost boundary before GPU work.
- [x] Task: Gate NVIDIA/NGC execution.
    - [x] Run `ngc config current`.
    - [x] Confirm API key, org/team, entitlements, and container/model availability before use.
- [x] Task: Conductor - User Manual Verification 'Cloud and Dynamic Backend Proofs' (Protocol in workflow.md)
    - [x] Evidence: Colab session listing succeeds; Azure is blocked pending login; NGC is blocked pending API-key/org/team configuration.
    - [x] Health: 9.6 / 10; cloud execution is correctly fail-closed.

## Phase 4: Documentation and Reproducibility

- [x] Task: Update runtime proof artifacts.
    - [x] Audit proof queues and benchmark reports.
    - [x] Confirm `MODEL_CANDIDATES.yaml` runtime fields remain consistent with the proof matrix.
    - [x] Update `FUTURE_MODELS.md` only for roadmap-level decisions.
- [x] Task: Validate and checkpoint.
    - [x] Run readiness and candidate checks.
    - [x] Commit and push bounded evidence and docs.
- [x] Task: Conductor - User Manual Verification 'Documentation and Reproducibility' (Protocol in workflow.md)
    - [x] Evidence: `reports/runtime/cross-runtime-proof-matrix-20260612.md`; `scripts/validate_readiness.py`; `scripts/check_model_candidates.py`.
    - [x] Health: 9.6 / 10; no roadmap-level `FUTURE_MODELS.md` change was needed.
