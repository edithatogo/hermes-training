# sentence-transformers Embedding Benchmark: embedding-qwen3-06b-smoke-20260612

Date: 2026-06-12T13:16:27.330020+00:00
Model: `Qwen/Qwen3-Embedding-0.6B`
Device: `cpu`
Cache root: `/Volumes/PortableSSD/huggingface`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Top-1 accuracy | 0.667 |
| Recall@3 | 1.000 |
| MRR | 0.833 |
| nDCG@3 | 0.877 |
| Embedding dims | 1024 |
| Embed latency p50 | 0.192s |
| Embed latency p95 | 1.231s |

## Cases

| Case | Top document | Pass |
|---|---|---:|
| metadata-database | target-sqlite | True |
| recency-preference | old-preference | False |
| benchmark-type | mem0-memory | True |

## Decision

`Qwen/Qwen3-Embedding-0.6B` is now runtime-proven on the local sentence-transformers path and is fast enough to keep in the mem0 candidate queue. It is not a default replacement because the smoke suite exposed the same recency-sensitive failure that the expanded retrieval gates are meant to catch.

Output: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-qwen3-06b-smoke-20260612`
