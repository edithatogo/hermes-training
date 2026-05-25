# Plan: mem0 Margin Rerank Live Smoke

## Phase 1: Wrapper Support

- [x] Task: expose the margin-gated reranker in `scripts/mem0_rerank_search.py`.
- [x] Task: add or update tests for the wrapper strategy choices.

## Phase 2: Runtime Recovery

- [~] Task: restore a responsive Ollama daemon with external SSD model storage.
- [~] Task: verify `ollama list` returns within a bounded check.

## Phase 3: Live Read-Only Smoke

- [ ] Task: run a read-only mem0 search through the margin-gated reranker.
- [x] Task: document the result and preserve the no-default-change decision.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 7.2 / 10
- Evidence: wrapper support is present and documented; no mem0 defaults changed.
- Gaps: local Ollama binds to `127.0.0.1:11434` but times out on `ollama list`
  and `/api/version`, so live mem0 smoke cannot be claimed.
