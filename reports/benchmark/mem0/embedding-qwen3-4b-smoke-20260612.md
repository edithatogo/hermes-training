# sentence-transformers Embedding Benchmark: embedding-qwen3-4b-smoke-20260612

Date: 2026-06-12T12:14:08.430083+00:00
Model: `Qwen/Qwen3-Embedding-4B`
Device: `cpu`
Cache root: `/Volumes/PortableSSD/huggingface`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Top-1 accuracy | 1.000 |
| Recall@3 | 1.000 |
| MRR | 1.000 |
| nDCG@3 | 1.000 |
| Embedding dims | 2560 |
| Embed latency p50 | 2.155s |
| Embed latency p95 | 11.578s |

## Cases

| Case | Top document | Pass |
|---|---|---:|
| metadata-database | target-sqlite | True |
| recency-preference | current-preference | True |
| benchmark-type | mem0-memory | True |

## Decision

`Qwen/Qwen3-Embedding-4B` is now load- and benchmark-proven from the external SSD cache. Keep it as a high-quality candidate, not the default, until a larger replay and collection migration plan justify replacing `mem0_nomic_768`.

Output: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-qwen3-4b-smoke-20260612`
