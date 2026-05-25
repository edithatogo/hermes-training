# Plan: BGE-M3 CPU Smoke

## Phase 1: Acquisition Check

- [x] Task: inspect SSD Hugging Face cache for BGE-M3.
- [x] Task: verify sentence-transformers load and one 1024-dim embedding.

## Phase 2: Benchmark

- [x] Task: run CPU embedding benchmark against
  `benchmarks/embeddings/memory_retrieval_suite.json`.
- [x] Task: record metrics, latency, and residual failure case.

## Phase 3: Decision

- [x] Task: update mem0 candidate status.
- [x] Task: update benchmark index and report.
- [x] Task: add a benchmark-script escape hatch for sentence-transformers
  teardown hangs.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: CPU benchmark completed and wrote outputs on SSD.
- Gaps: no live mem0 collection was created because BGE-M3 did not beat the
  baseline on this suite; teardown still needed manual process cleanup in this
  run.
- Decision: complete as CPU benchmark evidence, not default promotion.
