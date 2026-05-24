# Fixed Reranking Benchmark: fixed-rerank-lexical-overlap-expanded-20260524

Date: 2026-05-24T07:55:43.821689+00:00
Strategy: `lexical_overlap`
Model: ``

## Result

| Metric | Value |
|---|---:|
| Cases | 6 |
| Top-1 accuracy | 0.833 |
| Recall@3 | 1.000 |
| MRR | 0.917 |
| nDCG@3 | 0.938 |
| Recency conflict pass rate | 0.500 |
| Distractor resistance pass rate | 1.000 |
| Rerank latency p50 | 0.000s |

## Cases

| Case | Category | Top candidate | Pass |
|---|---|---|---:|
| current-embedding-preference | recency_conflict | current-preference | True |
| metadata-store-direct | direct_recall | target-sqlite | True |
| benchmark-distractor | distractor_resistance | mem0-memory | True |
| artifact-path-direct | direct_recall | target-exports | True |
| extractor-preference-update | recency_conflict | older-hermes | False |
| semantic-margin-beats-recency | distractor_resistance | target-collection | True |
