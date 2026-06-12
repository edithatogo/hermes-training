# LFM2-ColBERT + Qwen3-0.6B Reranking Benchmark: lfm2-colbert-qwen3-06b-rerank-20260612

Date: 2026-06-12T13:34:41.917385+00:00
Retriever source: `LiquidAI/LFM2-ColBERT-350M`
Reranker: `Qwen/Qwen3-Reranker-0.6B`
Strategy: `qwen3_causal_lm`
Device: `cpu`
Candidate suite: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/lfm2-colbert-expanded-derived-reranking-20260612/candidate-suite.json`

## Result

| Metric | Value |
|---|---:|
| Cases | 12 |
| Top-1 accuracy | 1.000 |
| Recall@3 | 1.000 |
| MRR | 1.000 |
| nDCG@3 | 1.000 |
| Recency conflict pass rate | 1.000 |
| Distractor resistance pass rate | 1.000 |
| Rerank latency p50 | 0.750s |
| Rerank latency p95 | 0.843s |

## Cases

| Case | Category | Top candidate | Pass |
|---|---|---|---:|
| metadata-database | direct_recall | target-sqlite | True |
| recency-preference | recency_conflict | current-preference | True |
| benchmark-type | distractor_resistance | mem0-memory | True |
| artifact-path-direct | direct_recall | target-exports | True |
| extractor-preference-update | recency_conflict | current-lfm2 | True |
| semantic-margin-beats-recency | distractor_resistance | target-collection | True |
| publication-gate | direct_recall | target-approval | True |
| adapter-promotion | direct_recall | target-v4 | True |
| azure-quota | distractor_resistance | target-quota | True |
| ollama-retest | direct_recall | target-after-upgrade | True |
| lfm25-guard | distractor_resistance | target-empty-response | True |
| storage-policy | direct_recall | target-evals | True |

## Decision

This is the strongest current mem0 quality/latency candidate path: LFM2-ColBERT provides fast high-recall retrieval on MPS, and Qwen3-Reranker-0.6B restores strict top-1 correctness with sub-second p50 reranking. Keep it opt-in until the live mem0 read wrapper supports the retriever-service shape, rollback behavior, and cold/warm latency monitoring.

Output: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/lfm2-colbert-qwen3-06b-rerank-20260612`
