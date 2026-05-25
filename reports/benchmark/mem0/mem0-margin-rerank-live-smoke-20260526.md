# mem0 Margin Rerank Live Smoke

Date: 2026-05-26

## Runtime Recovery

The previous live smoke was blocked by a stale Qdrant lock and an unresponsive
Ollama model root. The working recovery path is:

```bash
OLLAMA_MODELS=/Volumes/PortableSSD/Ollama/mem0-clean-models \
OLLAMA_HOST=127.0.0.1:11434 \
/opt/homebrew/bin/ollama serve
```

The clean SSD-backed root contains:

```text
nomic-embed-text:latest    0a109f422b47    274 MB
```

Validation:

- `GET /api/version` returned Ollama `0.24.0`.
- `ollama list` returned `nomic-embed-text:latest`.
- `/api/embeddings` returned a 768-dimensional vector.
- The stale Python process holding `/Users/doughnut/.mem0/qdrant/.lock` was
  stopped before the live mem0 smoke.

## Live Read-Only Wrapper Smoke

Command:

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy score_plus_created_at_rank_close_margin \
  --recency-weight 0.20 \
  --timeout-s 60
```

Result:

| Metric | Value |
|---|---:|
| Exit code | 0 |
| Latency | 2.873s |
| Input results | 1 |
| Strategy | `score_plus_created_at_rank_close_margin` |

Top result:

```text
Shared mem0 setup note: local mem0 is active with Ollama nomic-embed-text embeddings, raw storage by default, and LFM2 extraction configured but deferred until runner stability improves.
```

## Decision

The read-only wrapper path is validated for live mem0 search. This does not
change `~/.mem0/config.json`, the live default embedder, or the Qdrant
collection. Keep `mem0_nomic_768` as the default and use the wrapper for
reranked reads before considering any deeper integration.

LFM2 extraction is still deferred unless `sam860/LFM2:2.6b` is pulled into the
clean Ollama root and separately smoked.
