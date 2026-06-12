# LiquidAI LFM2 ColBERT Retriever Benchmark: retriever-lfm2-colbert-20260612

Date: 2026-06-12T11:33:39.829400+00:00
Model: `LiquidAI/LFM2-ColBERT-350M`
Runtime: `retriever-service (mps)`
Index: `mem0_lfm2_colbert_350m`
Base URL: `http://127.0.0.1:8765`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Top-1 accuracy | 1.000 |
| Recall@3 | 1.000 |
| MRR | 1.000 |
| nDCG@3 | 1.000 |
| Query latency p50 | 0.149s |
| Query latency p95 | 0.200s |

## Cases

| Case | Top document | Pass |
|---|---|---:|
| metadata-database | target-sqlite | True |
| recency-preference | current-preference | True |
| benchmark-type | mem0-memory | True |

## Interpretation

The late-interaction retriever completed the smoke fixture with a clean 1.000 on the small memory suite while running on MPS. That makes it a valid retriever candidate, but not yet a mem0 default:

- it still needs a larger replay suite
- it still needs a rollback comparison against the current dense path
- it should remain isolated from `mem0_nomic_768`

Raw outputs:

- `/Volumes/PortableSSD/hermes-evals/mem0-retriever-benchmark/retriever-lfm2-colbert-20260612/results.jsonl`
- `/Volumes/PortableSSD/hermes-evals/mem0-retriever-benchmark/retriever-lfm2-colbert-20260612/summary.json`
- `/Volumes/PortableSSD/hermes-evals/mem0-retriever-benchmark/retriever-lfm2-colbert-20260612/summary.md`
