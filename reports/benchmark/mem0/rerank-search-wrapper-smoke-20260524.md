# mem0 Reranked Search Wrapper Smoke

Date: 2026-05-24

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20
```

## Result

The wrapper successfully called the live `mem0 cmd search` path, parsed the CLI JSON, applied the same reranking implementation used by `scripts/evaluate_mem0_reranking.py`, and returned JSON.

The live store only returned one result for this query after benchmark cleanup:

- `Shared mem0 setup note: local mem0 is active with Ollama nomic-embed-text embeddings...`

This is expected. The wrapper is a read-only integration smoke, not a quality score. Quality evidence remains the saved benchmark replay in `reports/benchmark/mem0/recency-suite-20260524.md`.

## Decision

Keep `scripts/mem0_rerank_search.py` as a non-invasive candidate integration path. It can be used by agents that want reranked mem0 reads before the live mem0 default is changed.
