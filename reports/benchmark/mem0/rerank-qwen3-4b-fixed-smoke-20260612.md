# Fixed Reranking Benchmark: rerank-qwen3-4b-fixed-smoke-20260612

Date: 2026-06-12T12:32:39.969993+00:00
Strategy: `qwen3_causal_lm`
Model: `Qwen/Qwen3-Reranker-4B`
Device: `cpu`
Cache root: `/Volumes/PortableSSD/huggingface`

## Result

| Metric | Value |
|---|---:|
| Cases | 6 |
| Top-1 accuracy | 1.000 |
| Recall@3 | 1.000 |
| MRR | 1.000 |
| nDCG@3 | 1.000 |
| Recency conflict pass rate | 1.000 |
| Distractor resistance pass rate | 1.000 |
| Rerank latency p50 | 3.082s |
| Rerank latency p95 | 9.131s |

## Cases

| Case | Category | Top candidate | Pass |
|---|---|---|---:|
| current-embedding-preference | recency_conflict | current-preference | True |
| metadata-store-direct | direct_recall | target-sqlite | True |
| benchmark-distractor | distractor_resistance | mem0-memory | True |
| artifact-path-direct | direct_recall | target-exports | True |
| extractor-preference-update | recency_conflict | current-lfm2 | True |
| semantic-margin-beats-recency | distractor_resistance | target-collection | True |

## Decision

`Qwen/Qwen3-Reranker-4B` passes the fixed mem0 candidate suite, but CPU latency is materially higher than the existing Qwen3 0.6B and MLX BGE reranker candidates. Keep it as a quality ceiling and teacher/comparison reranker until a live replay or accelerated runtime beats the smaller candidates.

Output: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/rerank-qwen3-4b-fixed-smoke-20260612`
