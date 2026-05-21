# Plan: Qwen3 Strict Tool-Call Heldout Promotion

## Phase 1 - Track and Release Scaffold

- [x] Add Conductor spec, plan, metadata, and index for the strict heldout promotion lane.
- [x] Add publication readiness checklist under `reports/publication/qwen3-4b-strict-toolcall/`.
- [x] Update repo-level benchmarking and documentation plans with the strict heldout promotion rule.

## Phase 2 - Strict Dataset Training

- [x] Create or confirm the Qwen3 strict-tool-call training config for `gemma4/data/strict_tool_call`.
- [x] Run retraining from `Qwen/Qwen3-4B-MLX-4bit` with SSD-backed caches and output roots.
- [x] Record adapter path, effective trained tokens, final validation loss, peak memory, wall time, and command line.

## Phase 3 - Heldout Evaluation

- [x] Run `benchmarks/tool_call_local/heldout_suite.json` with `/no_think`.
- [x] Record strict pass rate, JSON validity, argument correctness, invalid-tool handling, and repair metrics.
- [x] Optionally record diagnostic empty-think-stripped metrics as informational only.
- [x] Preserve raw outputs under `$HERMES_EVAL_ROOT/tool-call-benchmark/<run-id>`.

## Phase 4 - Publication Decision

- [x] Update the strict-tool-call publication checklist with exact evidence paths.
- [x] Mark publication READY only if strict heldout pass rate is `1.000`.
- [x] Keep Hugging Face adapter, model-card, and dataset publication blocked for any strict heldout pass rate below `1.000`.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: training completed at 28,020 effective tokens with 3.785 GB peak memory; mirrored diagnostic pass reached 1.000 after empty-think stripping; held-out strict pass was 0.250 and publication stayed blocked.
- Decision: implementation proof is complete, but the adapter is not publishable.
