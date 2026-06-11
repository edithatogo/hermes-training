# Plan: Gemma 4 E4B MLX Runtime And Role Smoke

## Phase 1: Acquisition

- [x] Task: verify current Gemma 4 E4B QAT MLX package availability.
- [x] Task: acquire `mlx-community/gemma-4-E4B-it-qat-4bit` to the SSD-backed
  Hugging Face cache.

## Phase 2: Runtime And Role Gates

- [x] Task: run a one-case direct MLX loglikelihood smoke.
- [x] Task: run the 3-case BFCL-style local pilot with a bounded token cap.
- [x] Task: record the strict-format failure mode.

## Phase 3: Documentation And Validation

- [x] Task: update `MODEL_CANDIDATES.yaml`, `RUNTIME_FORMAT_PROOF_QUEUE.yaml`,
  `FUTURE_MODELS.md`, `HANDOFF.md`, and the hub track registry.
- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: MLX load/scoring completed, BFCL-style pilot completed, and the
  fail-closed blocker is explicit.
- Gaps: strict Hermes tool-call behavior is not present; this model should not
  be trained or promoted without prompt/profile repair evidence.
