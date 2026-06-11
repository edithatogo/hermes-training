# Plan: EXAONE 4.0 1.2B Runtime Smoke

## Phase 1: Candidate And Artifact Check

- [x] Task: verify EXAONE 4.0 1.2B MLX and GGUF package availability.
- [x] Task: acquire `mlx-community/exaone-4.0-1.2b-4bit` to the SSD cache.
- [x] Task: acquire `EXAONE-4.0-1.2B-Q4_K_M.gguf` to the SSD cache.

## Phase 2: Runtime Proof

- [x] Task: run direct MLX loglikelihood smoke and record the Transformers
  config blocker.
- [x] Task: run bounded `llama-completion` GGUF generation smoke.
- [x] Task: record timing, memory, warning, and non-compliant output.

## Phase 3: Documentation And Validation

- [x] Task: update `MODEL_CANDIDATES.yaml`, `RUNTIME_FORMAT_PROOF_QUEUE.yaml`,
  `FUTURE_MODELS.md`, `HANDOFF.md`, and the hub track registry.
- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: the MLX blocker is concrete and the official GGUF has a bounded
  runtime proof from SSD-backed artifacts.
- Gaps: no Hermes-compliant output, no endpoint proof, and no local-pilot score.
