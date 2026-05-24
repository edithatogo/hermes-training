# Fixed Reranking Benchmark: fixed-rerank-vector-expanded-20260524

Date: 2026-05-24T07:55:43.818869+00:00
Strategy: `vector`
Model: ``

## Result

| Metric | Value |
|---|---:|
| Cases | 6 |
| Top-1 accuracy | 0.667 |
| Recall@3 | 1.000 |
| MRR | 0.833 |
| nDCG@3 | 0.877 |
| Recency conflict pass rate | 0.000 |
| Distractor resistance pass rate | 1.000 |
| Rerank latency p50 | 0.000s |

## Cases

| Case | Category | Top candidate | Pass |
|---|---|---|---:|
| current-embedding-preference | recency_conflict | old-preference | False |
| metadata-store-direct | direct_recall | target-sqlite | True |
| benchmark-distractor | distractor_resistance | mem0-memory | True |
| artifact-path-direct | direct_recall | target-exports | True |
| extractor-preference-update | recency_conflict | older-hermes | False |
| semantic-margin-beats-recency | distractor_resistance | target-collection | True |
