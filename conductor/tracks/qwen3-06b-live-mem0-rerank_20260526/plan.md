# Plan: Qwen3 0.6B Live mem0 Rerank Wrapper

## Phase 1: Wrapper Support

- [x] Task: add `qwen3_causal_lm` as a read-only live wrapper strategy.
- [x] Task: expose model, device, max-length, and instruction arguments.
- [x] Task: keep heuristic strategies backward compatible.

## Phase 2: Tests and Live Smoke

- [x] Task: add unit coverage for live Qwen3 wrapper routing.
- [x] Task: run a live mem0 smoke against the clean SSD-backed Ollama root.

## Phase 3: Documentation and Gates

- [x] Task: document live smoke results and latency caveats.
- [x] Task: update handoff and mem0 benchmark documentation.
- [x] Task: run full validation before commit.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: live `mem0 cmd search` plus `Qwen/Qwen3-Reranker-0.6B` reranking
  exited 0, returned the expected active-collection memory, and reported
  `2.894s` search latency, `0.424s` scoring latency, and `13.413s` one-shot
  total latency.
- Gaps: production-quality use should keep the model warm; ONNX/Transformers.js
  runtime bridge remains future work.
