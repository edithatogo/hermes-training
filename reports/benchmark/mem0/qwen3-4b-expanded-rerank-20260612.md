# Fixed Reranking Benchmark: qwen3-4b-expanded-rerank-20260612

Date: 2026-06-12T13:12:23.827385+00:00
Strategy: `qwen3_causal_lm`
Model: `Qwen/Qwen3-Reranker-4B`
Device: `cpu`
Cache root: `/Volumes/PortableSSD/huggingface`
Candidate suite: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/qwen3-4b-expanded-derived-reranking-20260612/candidate-suite.json`

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
| Rerank latency p50 | 4.943s |
| Rerank latency p95 | 10.564s |

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

The 4B Qwen3 reranker fixes the expanded Qwen3-Embedding-4B miss and reaches the strict 1.000 gate, but p50/p95 latency is too high for an always-on local mem0 default. Keep it as a quality ceiling, teacher reranker, or opt-in high-precision mode until an accelerated runtime or service cache makes latency acceptable.

Output: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/qwen3-4b-expanded-rerank-20260612`
