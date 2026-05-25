# Qwen3 0.6B Live mem0 Rerank Smoke

Date: 2026-05-26

## Purpose

Validate `Qwen/Qwen3-Reranker-0.6B` against actual live `mem0 cmd search`
output without changing the mem0 config, Qdrant collection, embedder, or
extractor defaults.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --qwen3-max-length 4096 \
  --qwen3-local-files-only \
  --timeout-s 120
```

Runtime storage remained SSD-backed:

- Hugging Face cache: `/Volumes/PortableSSD/huggingface`
- Ollama model root: `/Volumes/PortableSSD/Ollama/mem0-clean-models`
- Evaluation/artifact root: `/Volumes/PortableSSD/hermes-evals`

## Result

| Metric | Value |
|---|---:|
| Exit code | 0 |
| Input results | 1 |
| mem0 search latency | 3.920s |
| Qwen3 rerank scoring latency | 0.216s |
| One-shot total latency | 12.093s |
| Top rerank score | 0.959 |

Top result:

```text
Shared mem0 setup note: local mem0 is active with Ollama nomic-embed-text embeddings, raw storage by default, and LFM2 extraction configured but deferred until runner stability improves.
```

## Decision

The read-only live wrapper path is proven for `Qwen/Qwen3-Reranker-0.6B`.
Do not promote it to the default live read path yet. The scorer itself is fast
once loaded, but a one-shot CLI invocation still pays model load time. The next
integration should keep the model warm through a local service or long-lived
agent helper, then compare live latency and quality against
`score_plus_created_at_rank_close_margin`.

The ONNX/Transformers.js candidate remains unproven as a runtime bridge; this
smoke used the source Hugging Face model through the Python causal-LM scorer.
