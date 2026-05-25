# mem0 Benchmark Index

| Kind | Run ID | Model/Tool | Raw Pass | Rerank Pass | Top-1 | Recall@k/3 | JSON Valid | Latency p50 | Output |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| embedding | embedding-nomic-openai-ollama-smoke-20260524 | nomic-embed-text:latest | 0.667 |  | 0.667 | 1.000 |  | 0.025 | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-openai-ollama-smoke-20260524` |
| embedding | embedding-nomic-smoke-20260524 | nomic-embed-text:latest | 0.667 |  | 0.667 | 1.000 |  | 0.021 | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-smoke-20260524` |
| embedding | embedding-bge-m3-cpu-smoke-20260526 | BAAI/bge-m3 | 0.667 |  | 0.667 | 1.000 |  | 0.098 | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-bge-m3-cpu-smoke-20260526` |
| extraction | extraction-hermes3-8b-expanded-examples-20260524 | hermes3:8b | 0.571 |  |  |  | 0.714 | 1.476 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes3-8b-expanded-examples-20260524` |
| extraction | extraction-hermes3-8b-expanded-strict-20260524 | hermes3:8b | 0.429 |  |  |  | 0.714 | 0.720 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes3-8b-expanded-strict-20260524` |
| extraction | extraction-hermes3-8b-smoke-20260524 | hermes3:8b | 0.333 |  |  |  | 0.333 | 1.031 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes3-8b-smoke-20260524` |
| extraction | extraction-lfm2-2-6b-expanded-examples-20260524 | sam860/LFM2:2.6b | 1.000 |  |  |  | 1.000 | 1.847 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-expanded-examples-20260524` |
| extraction | extraction-lfm2-2-6b-expanded-strict-20260524 | sam860/LFM2:2.6b | 0.571 |  |  |  | 1.000 | 0.758 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-expanded-strict-20260524` |
| extraction | extraction-lfm2-2-6b-prompt-file-20260524 | sam860/LFM2:2.6b | 1.000 |  |  |  | 1.000 | 0.866 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-prompt-file-20260524` |
| extraction | extraction-lfm2-2-6b-smoke-20260524 | sam860/LFM2:2.6b | 0.333 |  |  |  | 0.667 | 0.786 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-smoke-20260524` |
| memory | mem0-current-nomic-recency-20260524 | cmd | 0.400 |  | 0.400 | 1.000 |  | 2.890 | `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-20260524` |
| memory | mem0-current-nomic-smoke-20260524 | cmd | 0.667 |  | 0.667 | 1.000 |  | 3.388 | `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-smoke-20260524` |
| memory+rerank | mem0-current-nomic-recency-reranked-20260524 | cmd | 0.400 | 1.000 | 0.400 | 1.000 |  | 3.872 | `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-reranked-20260524` |
| reranking | fixed-rerank-created-at-rank-20260524 | score_plus_created_at_rank | 1.000 |  | 1.000 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-created-at-rank-20260524` |
| reranking | fixed-rerank-created-at-rank-expanded-20260524 | score_plus_created_at_rank | 1.000 |  | 1.000 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-created-at-rank-expanded-20260524` |
| reranking | fixed-rerank-lexical-overlap-20260524 | lexical_overlap | 1.000 |  | 1.000 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-lexical-overlap-20260524` |
| reranking | fixed-rerank-lexical-overlap-expanded-20260524 | lexical_overlap | 0.833 |  | 0.833 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-lexical-overlap-expanded-20260524` |
| reranking | fixed-rerank-vector-20260524 | vector | 0.667 |  | 0.667 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-vector-20260524` |
| reranking | fixed-rerank-vector-expanded-20260524 | vector | 0.667 |  | 0.667 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-vector-expanded-20260524` |

## Candidate Acquisition Notes

- `BAAI/bge-m3` is now acquired and CPU-benchmarked from the SSD cache, but it
  is not promoted because it matches the nomic top-1/recall result on the tiny
  suite while running slower and still missing the recency-preference case. Report:
  `reports/benchmark/mem0/embedding-bge-m3-acquisition-blocked-20260525.md`
