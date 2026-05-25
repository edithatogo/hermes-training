# mem0 Margin Rerank Live Smoke Blocker

Date: 2026-05-26

## Intended Smoke

Expose `score_plus_created_at_rank_close_margin` through the read-only mem0
search wrapper and run a live local query without changing `~/.mem0/config.json`
or the default `mem0_nomic_768` collection.

Command target:

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy score_plus_created_at_rank_close_margin \
  --recency-weight 0.20 \
  --timeout-s 60
```

## Result

The wrapper now exposes the margin-gated strategy, but the live mem0 smoke was
not run because local Ollama became unresponsive.

Observed behavior:

- `ollama serve` binds to `127.0.0.1:11434`.
- `ollama list` and `GET /api/version` time out.
- The issue reproduces against the existing SSD model stores and clean test
  model roots.
- Sampling the hung `ollama serve` process shows the main thread blocked in
  `open`.
- A completely reliable live mem0 query cannot be claimed from this runtime
  state.

No changes were made to:

- `~/.mem0/config.json`
- live default embedder `nomic-embed-text:latest`
- live Qdrant collection `mem0_nomic_768`

The hung Ollama server process was stopped after testing. The Homebrew
`homebrew.mxcl.ollama` service was also stopped so it would not keep respawning
an unresponsive server during validation.

## Decision

Keep the margin-gated reranker as the next read-only mem0 wrapper candidate,
but do not claim live mem0 validation until Ollama responsiveness is restored.

Next steps:

1. Restore a responsive Ollama daemon with `nomic-embed-text:latest` and
   `sam860/LFM2:2.6b`.
2. Run the wrapper command above.
3. Record raw wrapper output and latency.
4. Only after that, consider wiring the wrapper into agent read paths.
