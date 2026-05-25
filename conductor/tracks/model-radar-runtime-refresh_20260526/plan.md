# Plan: Model Radar and Runtime Refresh

## Phase 1: Latest Model Scan

- [x] Task: refresh Qwen3.7, Qwen3.6, Hermes 4.3, and LFM2-24B availability.
- [x] Task: record Qwen3.7 as still watchlist-only for local/open-weight work.
- [x] Task: record stronger Qwen3.6 GGUF/MLX and LFM2-24B quant options without
  starting new downloads.

## Phase 2: Runtime Decisions

- [x] Task: update the candidate matrix for Qwen3 v4, Qwen3.6, Hermes 4,
  LFM2-24B, and LM Studio runtime proof status.
- [x] Task: update runtime inventory language so completed proofs are not
  described as no-artifact blockers.
- [x] Task: update handoff next actions to remove completed LM Studio smoke.

## Phase 3: Benchmark Environment

- [x] Task: retain the official benchmark environment manifest.
- [x] Task: link the official harness environments from benchmark docs.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: current scan sources are recorded, runtime proof docs are linked,
  official benchmark environments are documented, and validation passes.
- Gaps: official BFCL/IFEval/lm-eval runs are still future execution work;
  Azure remains blocked by useful GPU quota; dataset publication remains
  separate.
- Decision: complete this refresh as documentation and gate alignment.
