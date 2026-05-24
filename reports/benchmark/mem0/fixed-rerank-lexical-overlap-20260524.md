# Fixed Reranking Benchmark: fixed-rerank-lexical-overlap-20260524

Date: 2026-05-24T07:35:26.260409+00:00
Strategy: `lexical_overlap`
Model: ``

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Top-1 accuracy | 1.000 |
| Recall@3 | 1.000 |
| MRR | 1.000 |
| nDCG@3 | 1.000 |
| Recency conflict pass rate | 1.000 |
| Distractor resistance pass rate | 1.000 |
| Rerank latency p50 | 0.000s |

## Cases

| Case | Category | Top candidate | Pass |
|---|---|---|---:|
| current-embedding-preference | recency_conflict | current-preference | True |
| metadata-store-direct | direct_recall | target-sqlite | True |
| benchmark-distractor | distractor_resistance | mem0-memory | True |
