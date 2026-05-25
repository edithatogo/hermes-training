# BGE Reranker v2 M3 MLX 8-bit Fixed-Suite Proof

Date: 2026-05-26

## Scope

Validate the verified Apple Silicon MLX reranker candidate
`flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit` as a bounded mem0 reranking
candidate. This proof adds only an offline fixed-suite scoring path. It does
not change `~/.mem0/config.json`, the default `mem0_nomic_768` collection, or
the guarded live read wrapper.

Update: the first harness used manually composed XLM-R separators and reached
1.000 on the fixed suite but only 0.917 on both expanded suites. The accepted
path uses the tokenizer's native paired input support, which passed all fixed
and expanded reranking suites.

## Command

```bash
HF_HUB_DISABLE_XET=1 ./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy mlx_cross_encoder \
  --model flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit \
  --mlx-max-length 1024 \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id rerank-flaglow-baai-bge-reranker-v2-m3-mlx-mxfp8-8bit-pairtok-fixed-20260526 \
  --output-dir /Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/rerank-flaglow-baai-bge-reranker-v2-m3-mlx-mxfp8-8bit-pairtok-fixed-20260526
```

The safetensors acquisition initially stalled through the default Hugging Face
path. Re-running the explicit acquisition with `HF_HUB_DISABLE_XET=1` completed
the 8-bit artifact and the benchmark then loaded from cache.

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
| Rerank latency p50 | 0.071s |
| Rerank latency p95 | 0.103s |

Expanded replay results:

| Suite | Top-1 | Recall@3 | Rerank p50 |
|---|---:|---:|---:|
| BGE-derived expanded | 1.000 | 1.000 | 0.077s |
| nomic-derived expanded | 1.000 | 1.000 | 0.091s |

Isolated live fixture:

| Strategy | Pass | Top-1 | Recall@3 | Rerank p50 |
|---|---:|---:|---:|---:|
| vector | 0.600 | 0.600 | 1.000 | 0.000s |
| score_plus_created_at_rank_close_margin | 0.800 | 0.800 | 1.000 | 0.000s |
| mlx_cross_encoder / 8-bit BGE | 1.000 | 1.000 | 1.000 | 0.145s |

Artifacts:

- Fixed summary: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/rerank-flaglow-baai-bge-reranker-v2-m3-mlx-mxfp8-8bit-pairtok-fixed-20260526/summary.json`
- BGE expanded summary: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/rerank-flaglow-baai-bge-reranker-v2-m3-mlx-mxfp8-8bit-pairtok-bge-expanded-20260526/summary.json`
- nomic expanded summary: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/rerank-flaglow-baai-bge-reranker-v2-m3-mlx-mxfp8-8bit-pairtok-nomic-expanded-20260526/summary.json`
- Isolated fixture summary: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-mlx-bge-reranker-v2-m3-8bit-20260526/summary.json`
- Run cards: `reports/benchmark/mem0/run-cards/`

## Decision

Promote this candidate from repo-ID verified to isolated-fixture proven. It is
now available as explicit `mlx-bge` mode in the guarded mem0 read wrapper and
Hermes mem0 tool with vector fallback. Keep the default mem0 config unchanged
until a broader daily-use latency probe justifies making this more automatic.
