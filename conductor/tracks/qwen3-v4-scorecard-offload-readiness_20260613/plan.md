# Plan: Qwen3 V4 Scorecard Offload Readiness

## Phase 1 - Readiness Checker

- [x] Task: Add a scorecard offload readiness checker.
  - [x] Read the no-limit scorecard plan.
  - [x] Inspect adapter metadata and file shape.
  - [x] Distinguish MLX-native adapters from HF/PEFT portable adapters.

## Phase 2 - Evidence

- [x] Task: Generate a cloud/offload readiness report.
- [x] Task: Add unit tests for blocked MLX and ready PEFT cases.
- [x] Task: Run focused tests and hub readiness validation.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: `scripts/check_scorecard_offload_readiness.py` reports the current v4 adapter as MLX-native and not exact-adapter portable to CUDA Colab/Azure; unit tests cover both blocked and ready paths.
- Gaps: A real cloud scorecard still needs a PEFT/Transformers export or a long local MLX resume window.
- Decision: Complete. The offload route is now explicit and fail-closed.
