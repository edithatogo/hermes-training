# sentence-transformers Embedding Benchmark: embedding-qwen3-4b-expanded-20260612

Date: 2026-06-12T13:09:46.114469+00:00
Model: `Qwen/Qwen3-Embedding-4B`
Device: `cpu`
Cache root: `/Volumes/PortableSSD/huggingface`

## Result

| Metric | Value |
|---|---:|
| Cases | 12 |
| Top-1 accuracy | 0.917 |
| Recall@3 | 1.000 |
| MRR | 0.958 |
| nDCG@3 | 0.969 |
| Embedding dims | 2560 |
| Embed latency p50 | 1.534s |
| Embed latency p95 | 2.811s |

## Cases

| Case | Top document | Pass |
|---|---|---:|
| metadata-database | target-sqlite | True |
| recency-preference | current-preference | True |
| benchmark-type | mem0-memory | True |
| artifact-path-direct | target-exports | True |
| extractor-preference-update | older-hermes | False |
| semantic-margin-beats-recency | target-collection | True |
| publication-gate | target-approval | True |
| adapter-promotion | target-v4 | True |
| azure-quota | target-quota | True |
| ollama-retest | target-after-upgrade | True |
| lfm25-guard | target-empty-response | True |
| storage-policy | target-evals | True |

## Decision

`Qwen/Qwen3-Embedding-4B` is a strong dense retrieval candidate, but the expanded suite keeps it below the current strict promotion gate because it misses the extractor-preference recency case. Keep it behind a separate 2560-dim collection and use reranking or recency-aware reads before considering default migration.

Output: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-qwen3-4b-expanded-20260612`
