# Plan: BGE-M3 Expanded Retrieval Benchmark

## Phase 1: Suite Expansion

- [x] Task: add a larger mem0-oriented embedding retrieval suite.
- [x] Task: add a structural unit test for the expanded suite.

## Phase 2: Benchmark Execution

- [x] Task: run BGE-M3 CPU benchmark from the SSD cache.
- [x] Task: attempt or document the current nomic baseline comparison.

## Phase 3: Decision and Documentation

- [x] Task: update benchmark reports and model candidate status.
- [x] Task: update the handoff with the next evidence-backed action.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: BGE-M3 expanded retrieval and derived reranker replay completed on
  SSD outputs; margin-gated reranker reached 1.000 on the expanded suite.
- Gaps: fresh nomic expanded re-run is pending because local Ollama was running
  but did not respond within the bounded check.
