# Plan: Qwen3.5 0.8B MLX Smoke

## Phase 1: Bounded Runtime Proof

- [x] Task: acquire `Qwen/Qwen3.5-0.8B` through the SSD-backed Hugging Face cache.
- [x] Task: run a one-case direct MLX loglikelihood smoke.

## Phase 2: Evidence And Queue Update

- [x] Task: record the markdown report and SSD output path.
- [x] Task: update `RUNTIME_FORMAT_PROOF_QUEUE.yaml`, `MODEL_CANDIDATES.yaml`,
  and handoff notes.

## Phase 3: Validation

- [x] Task: run unit tests, readiness validation, syntax checks, and commit the
  scoped proof.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: one-case MLX direct loglikelihood smoke passed with greedy match
  1.000, score latency 1.037s, and SSD-backed 1.7G model cache.
- Gaps: no adapter training, Hermes tool-call gate, or broader benchmark suite
  is claimed.

