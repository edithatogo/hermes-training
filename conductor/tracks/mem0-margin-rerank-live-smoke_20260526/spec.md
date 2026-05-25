# Specification: mem0 Margin Rerank Live Smoke

Expose the margin-gated recency reranker through the read-only mem0 search
wrapper and verify it against the live local mem0 path without changing the
default mem0 configuration.

Acceptance criteria:

- Add `score_plus_created_at_rank_close_margin` to the read-only wrapper CLI.
- Restore a responsive local Ollama daemon using SSD-backed model storage.
- Run a bounded read-only mem0 search through the wrapper.
- Record the live smoke result and any runtime caveats.
- Do not change `~/.mem0/config.json` or the live default embedder.

