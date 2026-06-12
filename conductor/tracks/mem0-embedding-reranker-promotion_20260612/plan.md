# mem0 Embedding and Reranker Promotion Execution Plan

## Phase 1: Baseline and Candidate Audit

- [ ] Task: Confirm current mem0 evidence.
    - [ ] Read existing mem0 benchmark reports and latency probes.
    - [ ] Confirm BGE-M3 baseline state and current integration path.
    - [ ] Identify candidate metadata that needs refreshed status or role text.
- [ ] Task: Confirm privacy and fixture boundaries.
    - [ ] Classify fixtures as synthetic, sanitized, or private.
    - [ ] Mark which benchmark jobs are eligible for Colab, Azure, or NVIDIA execution.
- [ ] Task: Conductor - User Manual Verification 'Baseline and Candidate Audit' (Protocol in workflow.md)

## Phase 2: Benchmark Expansion

- [ ] Task: Expand embedding comparison coverage.
    - [ ] Run BGE-M3 baseline with cold and warm timings.
    - [ ] Run Jina v5 small and text-matching MLX lanes.
    - [ ] Run EmbeddingGemma 300M where runtime proof is available.
    - [ ] Queue Qwen3 Embedding 4B only with appropriate runtime capacity.
- [ ] Task: Expand reranker comparison coverage.
    - [ ] Run isolated fixture rerank gates.
    - [ ] Run multi-result replay where existing harnesses support it.
    - [ ] Defer Qwen3 0.6B learned reranker until prompt/metadata and ONNX/CoreML proof are ready.
- [ ] Task: Use dynamic offload where appropriate.
    - [ ] Prefer Colab for sanitized multi-candidate sweeps.
    - [ ] Gate Azure and NGC usage behind auth, quota, and cost checks.
- [ ] Task: Conductor - User Manual Verification 'Benchmark Expansion' (Protocol in workflow.md)

## Phase 3: Default-Switch and Migration Policy

- [ ] Task: Define promotion thresholds.
    - [ ] Require quality improvement or clear latency/footprint advantage over BGE-M3.
    - [ ] Require local fallback compatibility before any default switch.
    - [ ] Require rollback instructions and collection migration notes.
- [ ] Task: Draft migration plan if a challenger wins.
    - [ ] Document collection rebuild impact.
    - [ ] Document mixed-index or staged migration behavior.
    - [ ] Document operator commands and rollback.
- [ ] Task: Conductor - User Manual Verification 'Default-Switch and Migration Policy' (Protocol in workflow.md)

## Phase 4: Documentation and Validation

- [ ] Task: Reconcile roadmap artifacts.
    - [ ] Update `FUTURE_MODELS.md`.
    - [ ] Update `MODEL_CANDIDATES.yaml`.
    - [ ] Update benchmark and latency reports.
- [ ] Task: Validate and checkpoint.
    - [ ] Run readiness checks.
    - [ ] Run candidate consistency checks if metadata changed.
    - [ ] Commit and push only reproducible, non-secret artifacts.
- [ ] Task: Conductor - User Manual Verification 'Documentation and Validation' (Protocol in workflow.md)
