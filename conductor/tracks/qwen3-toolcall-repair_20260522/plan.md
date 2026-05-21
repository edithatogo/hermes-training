# Plan: Qwen3 Tool-Call Repair Proof and Runtime Normalization Gate

## Phase 1 - Seed and Config

- [x] Add strict benchmark-mirrored training seed builder.
- [x] Generate tiny `gemma4/data/tool_call_splits` seed splits.
- [x] Add `gemma4/scripts/train_config.qwen3-4b.toolcall-repair.yaml`.
- [x] Dry-run the repair config under SSD-backed `scripts/env.sh`.

## Phase 2 - Training

- [x] Run 40-iteration MLX LoRA repair training.
- [x] Record trained tokens, final validation loss, peak memory, wall time, and adapter path.

## Phase 3 - Benchmark and Diagnostics

- [x] Run the strict local tool-call benchmark with `/no_think`.
- [x] Add diagnostic empty-think-stripped scoring without changing strict pass/fail.
- [x] Rescore the benchmark output to quantify wrapper noise separately from malformed tool-call output.

## Phase 4 - Documentation and Publication Decision

- [x] Add run card under `reports/publication/qwen3-4b-toolcall-repair/`.
- [x] Add Gemma/Qwen track eval summary.
- [x] Keep Hugging Face publication blocked.
- [x] Record next implementation: runtime empty-think normalizer, richer strict lane training, held-out benchmark.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: training completed at 10,603 tokens and 3.417 GB peak memory; strict benchmark remains 1/6; diagnostic empty-think-stripped pass rate is 5/6; publication blocker and next fix are explicit.
- Decision: implementation proof is complete, but the adapter is not publishable.
