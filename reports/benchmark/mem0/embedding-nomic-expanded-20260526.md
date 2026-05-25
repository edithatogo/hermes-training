# Ollama Embedding Benchmark: embedding-nomic-expanded-20260526

Date: 2026-05-25T16:23:23.223525+00:00
Model: `nomic-embed-text:latest`

## Result

| Metric | Value |
|---|---:|
| Cases | 12 |
| Top-1 accuracy | 0.833 |
| Recall@3 | 1.000 |
| MRR | 0.917 |
| nDCG@3 | 0.938 |
| Embedding dims | 768 |
| Embed latency p50 | 0.021s |
| Embed latency p95 | 0.087s |

## Cases

| Case | Top document | Pass |
|---|---|---:|
| metadata-database | target-sqlite | True |
| recency-preference | old-preference | False |
| benchmark-type | mem0-memory | True |
| artifact-path-direct | target-exports | True |
| extractor-preference-update | current-lfm2 | True |
| semantic-margin-beats-recency | target-collection | True |
| publication-gate | target-approval | True |
| adapter-promotion | target-v4 | True |
| azure-quota | target-quota | True |
| ollama-retest | lmstudio-validated | False |
| lfm25-guard | target-empty-response | True |
| storage-policy | target-evals | True |
