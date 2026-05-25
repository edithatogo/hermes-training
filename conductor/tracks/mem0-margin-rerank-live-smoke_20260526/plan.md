# Plan: mem0 Margin Rerank Live Smoke

## Phase 1: Wrapper Support

- [x] Task: expose the margin-gated reranker in `scripts/mem0_rerank_search.py`.
- [x] Task: add or update tests for the wrapper strategy choices.

## Phase 2: Runtime Recovery

- [x] Task: restore a responsive Ollama daemon with external SSD model storage.
- [x] Task: verify `ollama list` returns within a bounded check.

## Phase 3: Live Read-Only Smoke

- [x] Task: run a read-only mem0 search through the margin-gated reranker.
- [x] Task: document the result and preserve the no-default-change decision.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: live read-only mem0 wrapper smoke passed in 2.873s with
  `score_plus_created_at_rank_close_margin` using the clean SSD-backed Ollama
  root.
- Gaps: LFM2 extraction remains deferred until `sam860/LFM2:2.6b` is pulled and
  separately smoked in the clean root.
