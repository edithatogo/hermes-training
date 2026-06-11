# Plan: MiniCPM5 1B MLX Smoke

## Phase 1: Candidate Wiring

- [x] Task: verify official MiniCPM5 1B Hugging Face package IDs.
- [x] Task: add `openbmb/MiniCPM5-1B-MLX` to the model candidates.

## Phase 2: Runtime Proof

- [x] Task: acquire the MLX artifact through the SSD-backed Hugging Face cache.
- [x] Task: run a one-case direct MLX loglikelihood smoke.

## Phase 3: Evidence And Validation

- [x] Task: record the runtime report and queue update.
- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: one-case MLX direct loglikelihood smoke passed with greedy match
  1.000, score latency 0.600s, and 592M SSD cache footprint.
- Gaps: no Hermes adapter, extraction/tool-call smoke, or publication benchmark
  is claimed.
