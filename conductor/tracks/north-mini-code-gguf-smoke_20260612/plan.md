# Plan: North Mini Code GGUF Smoke

## Phase 1: Artifact And Runtime Proof

- [x] Task: acquire `North-Mini-Code-1.0-UD-Q4_K_M.gguf` through the
  SSD-backed Hugging Face cache.
- [x] Task: run a bounded local `llama-cli` smoke.

## Phase 2: Evidence And Queue Update

- [x] Task: record the runtime report and raw log path.
- [x] Task: update `RUNTIME_FORMAT_PROOF_QUEUE.yaml` and
  `MODEL_CANDIDATES.yaml` with the runtime blocker.

## Phase 3: Validation

- [x] Task: run candidate checks, runtime queue check, unit tests, readiness
  validation, and whitespace checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: the 18G GGUF artifact was acquired to the SSD and the local runtime
  failure was captured from a bounded `llama-cli` invocation.
- Gaps: current Homebrew `llama.cpp` cannot load `cohere2moe`; no model output,
  quality benchmark, or Hermes tool-call claim is available.
