# Retriever Service Benchmark: retriever-lfm2-colbert-expanded-20260612

Date: 2026-06-12T13:33:40.972036+00:00
Model: `LiquidAI/LFM2-ColBERT-350M`
Runtime: `retriever-service`
Device: `mps`
Cache root: `/Volumes/PortableSSD/huggingface`

## Result

| Metric | Value |
|---|---:|
| Cases | 12 |
| Top-1 accuracy | 0.917 |
| Recall@3 | 1.000 |
| MRR | 0.958 |
| nDCG@3 | 0.969 |
| Query latency p50 | 0.238s |
| Query latency p95 | 0.497s |

## Cases

| Case | Top document | Pass |
|---|---|---:|
| metadata-database | target-sqlite | True |
| recency-preference | current-preference | True |
| benchmark-type | mem0-memory | True |
| artifact-path-direct | target-exports | True |
| extractor-preference-update | current-lfm2 | True |
| semantic-margin-beats-recency | recent-colbert | False |
| publication-gate | target-approval | True |
| adapter-promotion | target-v4 | True |
| azure-quota | target-quota | True |
| ollama-retest | target-after-upgrade | True |
| lfm25-guard | target-empty-response | True |
| storage-policy | target-evals | True |

## Decision

`LiquidAI/LFM2-ColBERT-350M` is now expanded-suite proven as a fast late-interaction retriever with recall@3 `1.000`, but it does not meet the strict top-1 promotion gate by itself. Keep it as a separate retriever/index candidate and pair it with a reranker for default-quality comparisons.

Output: `/Volumes/PortableSSD/hermes-evals/mem0-retriever-benchmark/retriever-lfm2-colbert-expanded-20260612`
