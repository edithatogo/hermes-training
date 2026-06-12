# mem0 Embedding and Reranker Promotion Execution Plan

## Phase 1: Baseline and Candidate Audit

- [x] Task: Confirm current mem0 evidence.
    - [x] Read existing mem0 benchmark reports and latency probes.
    - [x] Confirm BGE-M3 baseline state and current integration path.
    - [x] Identify candidate metadata that needs refreshed status or role text.
    - Evidence: `README.md`, `mem0/BENCHMARKS.md`, `mem0/MODEL_CANDIDATES.yaml`, `reports/benchmark/mem0/validation/mem0-evidence-validation-20260526.json`, `reports/model-radar/mem0-candidate-queue.md`
- [x] Task: Confirm privacy and fixture boundaries.
    - [x] Classify fixtures as synthetic, sanitized, or private.
    - [x] Mark which benchmark jobs are eligible for Colab, Azure, or NVIDIA execution.
- [x] Task: Conductor - User Manual Verification 'Baseline and Candidate Audit' (Protocol in workflow.md)

## Phase 2: Benchmark Expansion

- [ ] Task: Expand embedding comparison coverage.
    - [x] Run BGE-M3 baseline with cold and warm timings.
    - [x] Run Jina v5 small and text-matching MLX lanes.
    - [ ] Run EmbeddingGemma 300M where runtime proof is available.
    - [ ] Queue Qwen3 Embedding 4B only with appropriate runtime capacity.
    - Blocker: `google/embeddinggemma-300m` returned a Hugging Face 403 on the first direct smoke; access is required before runtime proof can be collected.
    - Blocker: `Qwen/Qwen3-Embedding-4B` cached the repo locally but the direct MPS smoke stalled before writing a benchmark summary; defer until a cached or offloaded path is available.
    - Evidence: `reports/benchmark/mem0/run-cards/embedding-baai-bge-m3-refresh-20260612.md`, `reports/model-radar/mem0-candidate-queue.md`, `reports/benchmark/mem0/validation/mem0-evidence-validation-20260526.json`
- [ ] Task: Expand reranker comparison coverage.
    - [x] Run isolated fixture rerank gates.
    - [x] Run multi-result replay where existing harnesses support it.
    - [ ] Defer Qwen3 0.6B learned reranker until prompt/metadata and ONNX/CoreML proof are ready.
    - Evidence: `reports/benchmark/mem0/run-cards/mem0-replay-close-margin-fixed-refresh-20260612.md`, `reports/benchmark/mem0/run-cards/mem0-replay-close-margin-nomic-expanded-refresh-20260612.md`, `reports/benchmark/mem0/run-cards/mem0-replay-qwen3-causal-fixed-refresh-20260612.md`
- [ ] Task: Use dynamic offload where appropriate.
    - [ ] Prefer Colab for sanitized multi-candidate sweeps.
    - [ ] Gate Azure and NGC usage behind auth, quota, and cost checks.
- [ ] Task: Conductor - User Manual Verification 'Benchmark Expansion' (Protocol in workflow.md)

## Phase 3: Default-Switch and Migration Policy

- [x] Task: Define promotion thresholds.
    - [x] Require quality improvement or clear latency/footprint advantage over BGE-M3.
    - [x] Require local fallback compatibility before any default switch.
    - [x] Require rollback instructions and collection migration notes.
    - Evidence: `mem0/README.md`
- [x] Task: Draft migration plan if a challenger wins.
    - [x] Document collection rebuild impact.
    - [x] Document mixed-index or staged migration behavior.
    - [x] Document operator commands and rollback.
- [x] Task: Conductor - User Manual Verification 'Default-Switch and Migration Policy' (Protocol in workflow.md)

## Phase 4: Documentation and Validation

- [x] Task: Reconcile roadmap artifacts.
    - [x] Update `FUTURE_MODELS.md`.
    - [x] Update `MODEL_CANDIDATES.yaml`.
    - [x] Update benchmark and latency reports.
    - Evidence: `mem0/README.md`, `mem0/MODEL_CANDIDATES.yaml`, `reports/benchmark/mem0/run-cards/embedding-baai-bge-m3-refresh-20260612.md`, `reports/benchmark/mem0/run-cards/mem0-replay-close-margin-fixed-refresh-20260612.md`, `reports/benchmark/mem0/run-cards/mem0-replay-close-margin-nomic-expanded-refresh-20260612.md`, `reports/benchmark/mem0/run-cards/mem0-replay-qwen3-causal-fixed-refresh-20260612.md`, `reports/benchmark/mem0/validation/mem0-evidence-validation-20260526.json`
- [x] Task: Validate and checkpoint.
    - [x] Run readiness checks.
    - [x] Run candidate consistency checks if metadata changed.
    - [x] Commit and push only reproducible, non-secret artifacts.
- [x] Task: Conductor - User Manual Verification 'Documentation and Validation' (Protocol in workflow.md)
