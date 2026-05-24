# OpenAI-Compatible Embedding Benchmark: embedding-nomic-openai-ollama-smoke-20260524

Date: 2026-05-24

## Runtime

- Endpoint: `http://127.0.0.1:11434/v1/embeddings`
- Runtime: Ollama OpenAI-compatible API
- Model: `nomic-embed-text:latest`
- Suite: `benchmarks/embeddings/memory_retrieval_suite.json`
- Output: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-openai-ollama-smoke-20260524`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Top-1 accuracy | 0.667 |
| Recall@3 | 1.000 |
| MRR | 0.833 |
| nDCG@3 | 0.877 |
| Embedding dims | 768 |
| Embed latency p50 | 0.025s |
| Embed latency p95 | 0.048s |

## Case Notes

| Case | Top document | Pass |
|---|---|---:|
| `metadata-database` | `target-sqlite` | true |
| `recency-preference` | `old-preference` | false |
| `benchmark-type` | `mem0-memory` | true |

The OpenAI-compatible endpoint matches the native Ollama embedding runner on
ranking behavior for this suite. The remaining failure is the known recency
preference case, so this validates endpoint coverage rather than a new model
promotion.
