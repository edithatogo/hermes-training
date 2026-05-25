# Plan: Qwen3 0.6B Live mem0 Rerank Wrapper

## Phase 1: Wrapper Support

- [x] Task: add `qwen3_causal_lm` as a read-only live wrapper strategy.
- [x] Task: expose model, device, max-length, and instruction arguments.
- [x] Task: add a warm local HTTP helper for repeated Qwen3 reranking calls.
- [x] Task: keep heuristic strategies backward compatible.

## Phase 2: Tests and Live Smoke

- [x] Task: add unit coverage for live Qwen3 wrapper routing.
- [x] Task: run a live mem0 smoke against the clean SSD-backed Ollama root.
- [x] Task: prove warm-helper latency after the first service request.
- [x] Task: probe whether the live store has enough multi-result searches for
  a valid live reranker comparison.

## Phase 3: Documentation and Gates

- [x] Task: document live smoke results and latency caveats.
- [x] Task: update handoff and mem0 benchmark documentation.
- [x] Task: run full validation before commit.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: live `mem0 cmd search` plus `Qwen/Qwen3-Reranker-0.6B` reranking
  exited 0, returned the expected active-collection memory, and reported
  `3.920s` search latency, `0.216s` scoring latency, and `12.093s` one-shot
  total latency. The warm helper then reduced the second live request to
  `4.112s` total with `0.119s` Qwen scoring.
- Gaps: ONNX/Transformers.js runtime bridge remains future work. Multi-result
  live comparison needs an isolated fixture store or replay harness because the
  current default live store returns singleton results for broad probes.
