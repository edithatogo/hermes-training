# Plan: Gemma 4 E2B QAT GGUF Runtime Smoke

## Phase 1: Candidate Check

- [x] Task: verify current Gemma 4 E2B/E4B/12B QAT GGUF and MLX packages with
  the Hugging Face API.
- [x] Task: select the official E2B q4_0 text GGUF as the first bounded local
  proof.

## Phase 2: Runtime Smoke

- [x] Task: acquire `gemma-4-E2B_q4_0-it.gguf` to the SSD-backed Hugging Face
  cache.
- [x] Task: run bounded `llama-completion` generation smoke.
- [x] Task: record timing, memory, warnings, and empty-output behavior.

## Phase 3: Documentation And Validation

- [x] Task: update `MODEL_CANDIDATES.yaml`, `RUNTIME_FORMAT_PROOF_QUEUE.yaml`,
  `FUTURE_MODELS.md`, `HANDOFF.md`, and the hub track registry.
- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: official E2B q4_0 GGUF loads and exits cleanly through
  `llama-completion` from SSD-backed artifacts.
- Gaps: output was end-of-text only, so this is a runtime proof only and not a
  Hermes readiness claim.
