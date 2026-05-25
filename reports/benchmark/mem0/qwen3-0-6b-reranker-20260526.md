# Qwen3 0.6B mem0 Reranker Benchmark

Date: 2026-05-26

## Purpose

Validate a smaller learned reranker before attempting heavier Qwen3 4B or MLX
reranker paths for mem0 reads.

The public `onnx-community/Qwen3-Reranker-0.6B-ONNX` artifact targets
Transformers.js. For the Python benchmark harness, the source
`Qwen/Qwen3-Reranker-0.6B` model was scored as a causal LM by reading the
yes/no logits at the final token.

## Commands

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id rerank-qwen3-0-6b-fixed-20260526

./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --suite /Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-derived-reranking-20260526/candidate-suite.json \
  --run-id qwen3-0-6b-nomic-expanded-rerank-20260526

./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --suite /Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-derived-reranking-20260526/candidate-suite.json \
  --run-id qwen3-0-6b-bge-expanded-rerank-20260526
```

## Results

| Suite | Cases | Top-1 | Recall@3 | MRR | nDCG@3 | Recency conflict | Distractor resistance | p50 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fixed candidate | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.222s |
| Nomic expanded derived | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.314s |
| BGE-M3 expanded derived | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.334s |

## Decision

Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and
`sam860/LFM2:2.6b` as the live mem0 defaults.

Promote Qwen3 0.6B to the next read-reranker candidate. The next proof should
wrap live `mem0 search` output read-only and compare latency/results against
`score_plus_created_at_rank_close_margin`. The ONNX package still needs a
separate Transformers.js or ONNX runtime bridge before it can be called a
validated ONNX path.
