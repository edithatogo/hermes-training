# Qwen3 0.6B Warm-Service mem0 Rerank Smoke

Date: 2026-05-26

## Purpose

Prove that the live Qwen3 0.6B mem0 reranker can avoid repeated model-load
cost by routing scoring through a warm local helper.

## Commands

Start the Qwen3 helper:

```bash
source scripts/env.sh
./.venv/bin/python scripts/qwen3_reranker_service.py \
  --host 127.0.0.1 \
  --port 8765 \
  --model Qwen/Qwen3-Reranker-0.6B \
  --device auto \
  --local-files-only \
  --quiet
```

Run the live wrapper through the helper:

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --qwen3-local-files-only \
  --qwen3-server-url http://127.0.0.1:8765 \
  --timeout-s 120
```

## Result

| Run | mem0 search | Qwen3 scoring | Total | Top rerank score |
|---|---:|---:|---:|---:|
| First service request | 3.928s | 0.223s | 12.253s | 0.959 |
| Warm service request | 3.979s | 0.119s | 4.112s | 0.959 |

The top result remained the active mem0 setup memory:

```text
Shared mem0 setup note: local mem0 is active with Ollama nomic-embed-text embeddings, raw storage by default, and LFM2 extraction configured but deferred until runner stability improves.
```

## Decision

The warm helper removes the major Qwen3 model-load penalty for repeated live
reads. The bottleneck is now the live mem0 search call itself, not the learned
reranker. Keep this path as a candidate integration layer and compare it against
`score_plus_created_at_rank_close_margin` on multi-result live searches before
changing any default mem0 behavior.

The helper is still local-only and read-only. It does not write memories, change
Qdrant collections, or modify `~/.mem0/config.json`.
