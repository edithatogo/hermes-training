# Plan: Nomic Expanded Retrieval and Reranker Replay

## Phase 1: Runtime and Dense Retrieval

- [x] Task: start clean SSD-backed Ollama and verify `nomic-embed-text:latest`.
- [x] Task: run the expanded embedding retrieval suite for `nomic-embed-text:latest`.

## Phase 2: Derived Reranking

- [x] Task: build the fixed reranking suite from the nomic expanded results.
- [x] Task: replay vector, recency, margin-gated recency, and lexical strategies.

## Phase 3: Documentation and Gates

- [x] Task: document the comparison and no-default-change decision.
- [x] Task: update benchmark index, run-card index, mem0 radar, reranking docs,
  and handoff.
- [x] Task: run validation and leave the tree ready to push.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: `embedding-nomic-expanded-20260526` reached top-1 0.833 /
  recall@3 1.000; `nomic-expanded-close-margin-rerank-20260526` reached top-1
  0.917 with recency conflict and distractor resistance both 1.000.
- Gaps: one direct semantic miss remains (`ollama-retest`), so learned reranker
  and future embedder candidates still need comparison.
