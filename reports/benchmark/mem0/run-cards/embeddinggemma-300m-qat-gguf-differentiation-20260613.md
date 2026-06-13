# mem0 Run Card

Date: 2026-06-12T23:59:09.961631+00:00
Run ID: embeddinggemma-300m-qat-gguf-differentiation-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embeddinggemma-300m-qat-gguf-differentiation-20260613/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | embedder |
| Model/tool | `lmstudio-community/embeddinggemma-300m-qat-GGUF` |
| Runtime | llama-cpp-embedding |
| Endpoint | |
| Collection or index | |
| Embedding dims | 768 |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embeddinggemma-300m-qat-gguf-differentiation-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_llama_cpp_embedding_benchmark.py \
  --model lmstudio-community/embeddinggemma-300m-qat-GGUF \
  --model-path /Volumes/PortableSSD/huggingface/hub/models--lmstudio-community--embeddinggemma-300m-qat-GGUF/snapshots/a81b371598d25d26b714ab9b14948ce8ca375547/embeddinggemma-300m-qat-Q4_0.gguf \
  --ctx-size 512 \
  --pooling mean \
  --embd-normalize 2 \
  --suite benchmarks/embeddings/memory_retrieval_differentiation_suite.json \
  --run-id embeddinggemma-300m-qat-gguf-differentiation-20260613
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 1.000 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 1.000 |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 1.154 |
| Search/embed/extract latency p95 | 1.182 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The embedding benchmark passed the suite at the current 768-dim collection shape, but default promotion still needs live mem0 add/search latency, rollback, and collection compatibility proof.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
