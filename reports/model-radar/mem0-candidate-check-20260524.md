# mem0 Candidate Check

Date: 2026-05-24

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/check_mem0_model_candidates.py --check-hf
```

## Result

| Candidate | Role | Status | Hugging Face result | Modified | Notes |
|---|---|---|---|---|---|
| `nomic-embed-text:latest` | embedder | working-default | skipped | n/a | Ollama-style id; current local default. |
| `BAAI/bge-m3` | embedder | candidate | exists | 2024-07-03 | MIT; strong dense/sparse/multivector baseline. |
| `jinaai/jina-embeddings-v4` | embedder | candidate | exists | 2026-04-08 | Multimodal/multilingual embedding candidate. |
| `Qwen/Qwen3-Embedding-4B` | embedder | candidate | exists | 2025-06-20 | Apache-2.0; local runtime and memory proof needed. |
| `Qwen/Qwen3-Reranker-4B` | reranker | candidate | exists | 2026-04-16 | Apache-2.0; likely useful for recency/distractor ranking after dense retrieval. |
| `LiquidAI/LFM2-ColBERT-350M` | retriever | candidate | exists | 2026-05-05 | ColBERT/late-interaction candidate; requires separate index/API shape. |
| `sam860/LFM2:2.6b` | extractor | working-default | skipped | n/a | Ollama-style id; current mem0 LLM/extractor. |
| `hermes3:8b` | extractor | installed-baseline | skipped | n/a | Ollama-style id; installed local Hermes extractor baseline. |
| `NousResearch/Hermes-4-14B` | extractor | runtime-proof-needed | exists | 2026-01-09 | Hermes-aligned extraction/teacher candidate once a local runtime artifact is available. |

## Decision

Keep `nomic-embed-text:latest` as the rollback embedder and `sam860/LFM2:2.6b` as the rollback extractor. The next candidate work should be:

1. Add a recency-aware post-ranker over current mem0 results.
2. Test `BAAI/bge-m3` in a separate `mem0_bge_m3_1024` collection.
3. Test `Qwen/Qwen3-Reranker-4B` on fixed candidate sets before putting it in the live mem0 path.
4. Treat `LiquidAI/LFM2-ColBERT-350M` as a separate retriever service, not a Qdrant dense-vector swap.

