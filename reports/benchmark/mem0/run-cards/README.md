# mem0 Run Cards

Run cards turn raw benchmark summaries into reproducible candidate records.
Use them when comparing a new embedder, extractor, reranker, retriever, or
runtime endpoint against the current mem0 default.

## Current Cards

| Run | Role | Decision |
|---|---|---|
| [mem0-current-nomic-smoke-20260524](./mem0-current-nomic-smoke-20260524.md) | memory | keep testing |
| [mem0-current-nomic-recency-reranked-20260524](./mem0-current-nomic-recency-reranked-20260524.md) | memory+rerank | keep testing |
| [embedding-nomic-openai-ollama-smoke-20260524](./embedding-nomic-openai-ollama-smoke-20260524.md) | embedder endpoint | keep testing |
| [extraction-lfm2-2-6b-smoke-20260524](./extraction-lfm2-2-6b-smoke-20260524.md) | extractor | keep testing |
| [extraction-hermes3-8b-smoke-20260524](./extraction-hermes3-8b-smoke-20260524.md) | extractor | keep testing |
| [fixed-rerank-vector-20260524](./fixed-rerank-vector-20260524.md) | reranker baseline | keep testing |
| [fixed-rerank-created-at-rank-20260524](./fixed-rerank-created-at-rank-20260524.md) | reranker baseline | keep testing |
| [fixed-rerank-lexical-overlap-20260524](./fixed-rerank-lexical-overlap-20260524.md) | reranker baseline | keep testing |
| [fixed-rerank-vector-expanded-20260524](./fixed-rerank-vector-expanded-20260524.md) | reranker baseline | keep testing |
| [fixed-rerank-created-at-rank-expanded-20260524](./fixed-rerank-created-at-rank-expanded-20260524.md) | reranker baseline | keep testing |
| [fixed-rerank-lexical-overlap-expanded-20260524](./fixed-rerank-lexical-overlap-expanded-20260524.md) | reranker baseline | keep testing |
| [extraction-lfm2-2-6b-expanded-examples-20260524](./extraction-lfm2-2-6b-expanded-examples-20260524.md) | extractor | keep testing |
| [extraction-hermes3-8b-expanded-examples-20260524](./extraction-hermes3-8b-expanded-examples-20260524.md) | extractor | keep testing |
| [extraction-lfm2-2-6b-prompt-file-20260524](./extraction-lfm2-2-6b-prompt-file-20260524.md) | extractor | keep testing |
| [extraction-lfm2-2-6b-clean-root-20260526](./extraction-lfm2-2-6b-clean-root-20260526.md) | extractor | keep testing |
| [embedding-nomic-expanded-20260526](./embedding-nomic-expanded-20260526.md) | embedder | keep testing |
| [nomic-expanded-vector-rerank-20260526](./nomic-expanded-vector-rerank-20260526.md) | reranker baseline | keep testing |
| [nomic-expanded-created-at-rank-20260526](./nomic-expanded-created-at-rank-20260526.md) | reranker baseline | keep testing |
| [nomic-expanded-lexical-rerank-20260526](./nomic-expanded-lexical-rerank-20260526.md) | reranker baseline | keep testing |
| [nomic-expanded-close-margin-rerank-20260526](./nomic-expanded-close-margin-rerank-20260526.md) | reranker candidate | keep testing |

## Generate

```bash
source scripts/env.sh
./.venv/bin/python scripts/create_mem0_run_card.py \
  /Volumes/PortableSSD/hermes-evals/<benchmark-kind>/<run-id>/summary.json \
  --output reports/benchmark/mem0/run-cards/<run-id>.md
```
