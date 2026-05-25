# mem0 Benchmark Index

| Kind | Run ID | Model/Tool | Raw Pass | Rerank Pass | Top-1 | Recall@k/3 | JSON Valid | Latency p50 | Output |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| embedding | embedding-bge-m3-cpu-expanded-20260526 | BAAI/bge-m3 | 0.917 |  | 0.917 | 1.000 |  | 0.097 | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-bge-m3-cpu-expanded-20260526` |
| embedding | embedding-bge-m3-cpu-smoke-20260526 | BAAI/bge-m3 | 0.667 |  | 0.667 | 1.000 |  | 0.098 | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-bge-m3-cpu-smoke-20260526` |
| embedding | embedding-bge-m3-mps-smoke-20260526 | BAAI/bge-m3 | 0.667 |  | 0.667 | 1.000 |  | 0.126 | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-bge-m3-mps-smoke-20260526` |
| embedding | embedding-nomic-expanded-20260526 | nomic-embed-text:latest | 0.833 |  | 0.833 | 1.000 |  | 0.021 | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-expanded-20260526` |
| embedding | embedding-nomic-openai-ollama-smoke-20260524 | nomic-embed-text:latest | 0.667 |  | 0.667 | 1.000 |  | 0.025 | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-openai-ollama-smoke-20260524` |
| embedding | embedding-nomic-smoke-20260524 | nomic-embed-text:latest | 0.667 |  | 0.667 | 1.000 |  | 0.021 | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-smoke-20260524` |
| extraction | extraction-hermes3-8b-expanded-examples-20260524 | hermes3:8b | 0.571 |  |  |  | 0.714 | 1.476 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes3-8b-expanded-examples-20260524` |
| extraction | extraction-hermes3-8b-expanded-strict-20260524 | hermes3:8b | 0.429 |  |  |  | 0.714 | 0.720 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes3-8b-expanded-strict-20260524` |
| extraction | extraction-hermes3-8b-smoke-20260524 | hermes3:8b | 0.333 |  |  |  | 0.333 | 1.031 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes3-8b-smoke-20260524` |
| extraction | extraction-lfm2-2-6b-clean-root-20260526 | sam860/LFM2:2.6b | 1.000 |  |  |  | 1.000 | 0.874 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-clean-root-20260526` |
| extraction | extraction-lfm2-2-6b-expanded-examples-20260524 | sam860/LFM2:2.6b | 1.000 |  |  |  | 1.000 | 1.847 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-expanded-examples-20260524` |
| extraction | extraction-lfm2-2-6b-expanded-strict-20260524 | sam860/LFM2:2.6b | 0.571 |  |  |  | 1.000 | 0.758 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-expanded-strict-20260524` |
| extraction | extraction-lfm2-2-6b-prompt-file-20260524 | sam860/LFM2:2.6b | 1.000 |  |  |  | 1.000 | 0.866 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-prompt-file-20260524` |
| extraction | extraction-lfm2-2-6b-smoke-20260524 | sam860/LFM2:2.6b | 0.333 |  |  |  | 0.667 | 0.786 | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-smoke-20260524` |
| memory | mem0-current-nomic-recency-20260524 | cmd | 0.400 |  | 0.400 | 1.000 |  | 2.890 | `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-20260524` |
| memory | mem0-current-nomic-smoke-20260524 | cmd | 0.667 |  | 0.667 | 1.000 |  | 3.388 | `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-smoke-20260524` |
| memory+rerank | mem0-current-nomic-recency-reranked-20260524 | cmd | 0.400 | 1.000 | 0.400 | 1.000 |  | 3.872 | `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-reranked-20260524` |
| memory+rerank | mem0-fixture-close-margin-recency-20260526 | hermes_fixture | 0.400 | 1.000 | 0.400 | 1.000 |  | 2.862 | `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-fixture-close-margin-recency-20260526` |
| memory+rerank | mem0-fixture-qwen3-06b-recency-20260526 | hermes_fixture | 0.400 | 1.000 | 0.400 | 1.000 |  | 2.867 | `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-fixture-qwen3-06b-recency-20260526` |
| memory+rerank | guarded-close-margin-read-wrapper-20260526 | score_plus_created_at_rank_close_margin | 0.500 | 1.000 | 0.500 | 1.000 |  | 2.890 | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/guarded-close-margin-read-wrapper-20260526` |
| memory+rerank | mem0-isolated-fixture-rerank-comparison-20260526 | Qwen/Qwen3-Reranker-0.6B | 0.400 | 1.000 | 1.000 | 1.000 |  | 0.495 | `reports/benchmark/mem0/mem0-isolated-fixture-rerank-comparison-20260526.md` |
| memory+rerank | mem0-guarded-read-wrapper-smoke-20260526 | score_plus_created_at_rank_close_margin |  |  |  |  |  | 2.865 | `reports/benchmark/mem0/mem0-guarded-read-wrapper-smoke-20260526.md` |
| memory+rerank | mem0-read-cache-close-margin-20260526 | score_plus_created_at_rank_close_margin |  |  |  |  |  | 0.000 | `reports/benchmark/mem0/mem0-read-cache-close-margin-20260526.md` |
| memory+rerank | hermes-mem0-plugin-smoke-20260526 | hermes_mem0_read plugin |  |  |  |  |  | 3.970 | `reports/benchmark/mem0/hermes-mem0-plugin-smoke-20260526.md` |
| memory+rerank | hermes-mem0-tool-smoke-20260526 | score_plus_created_at_rank_close_margin |  |  |  |  |  | 0.000 | `reports/benchmark/mem0/hermes-mem0-tool-smoke-20260526.md` |
| memory+rerank | mem0-read-ux-close-margin-20260526 | score_plus_created_at_rank_close_margin |  |  |  |  |  | 2.897 | `reports/benchmark/mem0/mem0-read-ux-close-margin-20260526.md` |
| memory+rerank | live-multiretrieval-readiness-20260526 | cmd |  |  |  |  |  |  | `reports/benchmark/mem0/live-multiretrieval-readiness-20260526.md` |
| memory+rerank | mem0-rerank-replay-comparison-20260526 | Qwen/Qwen3-Reranker-0.6B |  |  | 1.000 | 1.000 |  | 0.250 | `reports/benchmark/mem0/mem0-rerank-replay-comparison-20260526.md` |
| memory+rerank | mem0-live-fixture-qwen3-multiretrieval-rerank-20260526 | isolated fixture / Qwen/Qwen3-Reranker-0.6B | 0.667 | 1.000 | 0.667 | 1.000 |  | 2.886 | `reports/benchmark/mem0/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526.md` |
| memory+rerank | qwen3-0-6b-live-rerank-smoke-20260526 | Qwen/Qwen3-Reranker-0.6B |  |  |  |  |  | 12.093 | `reports/benchmark/mem0/qwen3-0-6b-live-rerank-smoke-20260526.md` |
| memory+rerank | qwen3-0-6b-warm-service-rerank-smoke-20260526 | Qwen/Qwen3-Reranker-0.6B |  |  |  |  |  | 4.112 | `reports/benchmark/mem0/qwen3-0-6b-warm-service-rerank-smoke-20260526.md` |
| reranking | bge-m3-expanded-close-margin-rerank-20260526 | score_plus_created_at_rank_close_margin | 1.000 |  | 1.000 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-close-margin-rerank-20260526` |
| reranking | bge-m3-expanded-created-at-rank-20260526 | score_plus_created_at_rank | 0.917 |  | 0.917 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-created-at-rank-20260526` |
| reranking | bge-m3-expanded-lexical-rerank-20260526 | lexical_overlap | 0.917 |  | 0.917 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-lexical-rerank-20260526` |
| reranking | bge-m3-expanded-vector-rerank-20260526 | vector | 0.917 |  | 0.917 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-vector-rerank-20260526` |
| reranking | fixed-rerank-created-at-rank-20260524 | score_plus_created_at_rank | 1.000 |  | 1.000 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-created-at-rank-20260524` |
| reranking | fixed-rerank-created-at-rank-expanded-20260524 | score_plus_created_at_rank | 1.000 |  | 1.000 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-created-at-rank-expanded-20260524` |
| reranking | fixed-rerank-lexical-overlap-20260524 | lexical_overlap | 1.000 |  | 1.000 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-lexical-overlap-20260524` |
| reranking | fixed-rerank-lexical-overlap-expanded-20260524 | lexical_overlap | 0.833 |  | 0.833 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-lexical-overlap-expanded-20260524` |
| reranking | fixed-rerank-vector-20260524 | vector | 0.667 |  | 0.667 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-vector-20260524` |
| reranking | fixed-rerank-vector-expanded-20260524 | vector | 0.667 |  | 0.667 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-vector-expanded-20260524` |
| reranking | nomic-expanded-close-margin-rerank-20260526 | score_plus_created_at_rank_close_margin | 0.917 |  | 0.917 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-close-margin-rerank-20260526` |
| reranking | nomic-expanded-created-at-rank-20260526 | score_plus_created_at_rank | 0.750 |  | 0.750 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-created-at-rank-20260526` |
| reranking | nomic-expanded-lexical-rerank-20260526 | lexical_overlap | 0.917 |  | 0.917 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-lexical-rerank-20260526` |
| reranking | nomic-expanded-vector-rerank-20260526 | vector | 0.833 |  | 0.833 | 1.000 |  | 0.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-vector-rerank-20260526` |
| reranking | qwen3-0-6b-bge-expanded-rerank-20260526 | Qwen/Qwen3-Reranker-0.6B | 1.000 |  | 1.000 | 1.000 |  | 0.334 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/qwen3-0-6b-bge-expanded-rerank-20260526` |
| reranking | qwen3-0-6b-nomic-expanded-rerank-20260526 | Qwen/Qwen3-Reranker-0.6B | 1.000 |  | 1.000 | 1.000 |  | 0.314 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/qwen3-0-6b-nomic-expanded-rerank-20260526` |
| reranking | qwen3-0-6b-onnx-transformersjs-bridge-20260526 | onnx-community/Qwen3-Reranker-0.6B-ONNX |  |  | 0.000 | 0.000 |  | 0.000 | `reports/benchmark/mem0/qwen3-0-6b-onnx-transformersjs-bridge-20260526.md` |
| reranking | rerank-qwen3-0-6b-fixed-20260526 | Qwen/Qwen3-Reranker-0.6B | 1.000 |  | 1.000 | 1.000 |  | 0.222 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/rerank-qwen3-0-6b-fixed-20260526` |
