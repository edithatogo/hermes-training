# Plan: mem0 Isolated Fixture Rerank Gate

## Phase 1: Fixture Runner

- [x] Task: add a synthetic multi-result fixture suite.
- [x] Task: add an isolated `MEM0_CONFIG_PATH` runner with output-local Qdrant
  and history paths.
- [x] Task: add unit coverage for config isolation, relevance annotation, and
  run-card command generation.

## Phase 2: Benchmark

- [x] Task: run the isolated fixture without Qwen3 to verify live multi-result
  retrieval.
- [x] Task: run the warm Qwen3 comparison against the same fixture shape.
- [x] Task: stop the warm reranker service after validation.

## Phase 3: Documentation

- [x] Task: document the benchmark result and decision.
- [x] Task: update mem0 docs, model radar, run-card index, and handoff.
- [x] Task: run validation and push.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: isolated live fixture returned 3-5 candidates per query; close-margin passed at `1.000`; warm Qwen3 remained at `0.667` and was not promoted.
- Gaps: Qwen3 needs prompt/metadata work before another live recency fixture gate.
