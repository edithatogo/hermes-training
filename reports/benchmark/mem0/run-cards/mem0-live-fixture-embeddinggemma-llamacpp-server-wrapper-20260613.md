# mem0 Run Card

Date: 2026-06-13T00:17:29.619282+00:00
Run ID: mem0-live-fixture-embeddinggemma-llamacpp-server-wrapper-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-embeddinggemma-llamacpp-server-wrapper-20260613/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | memory+embedder fixture |
| Model/tool | `cmd` |
| Runtime | openai embedder + vector |
| Endpoint | `http://127.0.0.1:8095/v1` |
| Collection or index | `mem0_fixture_mem0_live_fixture_embeddinggemma_llamacpp_server_wrapper_2026061` |
| Embedding dims | 768 |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-embeddinggemma-llamacpp-server-wrapper-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_with_llama_cpp_embedding_server.py \
  --model-path /Volumes/PortableSSD/huggingface/hub/models--lmstudio-community--embeddinggemma-300m-qat-GGUF/snapshots/a81b371598d25d26b714ab9b14948ce8ca375547/embeddinggemma-300m-qat-Q4_0.gguf \
  --port 8095 \
  --parallel 1 \
  --run-id embeddinggemma-server-wrapper-mem0-fixture-20260613 \
  -- \
./.venv/bin/python scripts/run_mem0_isolated_fixture_rerank.py \
  --keep-fixture \
  --embedder-provider openai \
  --embedder-model embeddinggemma-300m-qat-Q4_0.gguf \
  --embedder-base-url http://127.0.0.1:8095/v1 \
  --embedding-dims 768 \
  --skip-qwen3 \
  --suite benchmarks/mem0_memory/live_fixture_differentiation_suite.json \
  --run-id mem0-live-fixture-embeddinggemma-llamacpp-server-wrapper-20260613
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.909 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.909 |
| Recency conflict pass rate | 1.000 |
| Distractor resistance pass rate | 0.750 |
| JSON validity rate |  |
| Add latency p50 | 2.957 |
| Search/embed/extract latency p50 | 2.971 |
| Search/embed/extract latency p95 | 3.457 |
| Rerank latency p50 | 0.000 |

## Strategy Comparison

| Strategy | Pass | Top-1 | Recall@3 | MRR | nDCG@3 | p50 rerank |
|---|---:|---:|---:|---:|---:|---:|
| `vector` | 0.909 | 0.909 | 1.000 | 0.955 | 0.966 | 0.000 |
| `score_plus_created_at_rank_close_margin` | 0.909 | 0.909 | 1.000 | 0.939 | 0.955 | 0.000 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The isolated fixture did not prove strict multi-result top-1 behavior and should remain a comparison baseline.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
