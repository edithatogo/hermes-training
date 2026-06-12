# Hermes mem0 Tool ColBERT + Qwen3 Fixture Smoke: 2026-06-12

Run ID: `hermes-tool-colbert-qwen3-fixture-smoke-20260612`
Date: 2026-06-12
Tool: `scripts/hermes_mem0_tool.py`
Mode: `colbert-qwen3`
Retriever: `LiquidAI/LFM2-ColBERT-350M` service on `http://127.0.0.1:8765`
Reranker: `Qwen/Qwen3-Reranker-0.6B`
Fixture: `benchmarks/embeddings/memory_retrieval_expanded_suite.json`

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/hermes_mem0_tool.py \
  --query "Which collection stores the current mem0 vectors?" \
  --mode colbert-qwen3 \
  --document-fixture benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --retriever-service-url http://127.0.0.1:8765 \
  --retriever-top-k 8 \
  --qwen3-device cpu \
  --qwen3-max-length 1024 \
  --qwen3-local-files-only \
  --timeout-s 120
```

## Result

| Metric | Value |
|---|---:|
| Tool result | `ok: true` |
| Read-only | `true` |
| Mutates mem0 config | `false` |
| Input candidates | 8 |
| Total latency | 10.243s |
| ColBERT retrieval latency | 0.703s |
| Qwen3 rerank latency | 4.927s |

Top result:

| Rank | ID | Memory | Retriever score | Rerank score |
|---:|---|---|---:|---:|
| 1 | `target-collection` | The active mem0 Qdrant collection is mem0_nomic_768. | 30.214237 | 0.993130 |

## Decision

The Hermes-facing command wrapper can now exercise the strongest current mem0 candidate path without changing mem0 defaults: fixture-backed LFM2-ColBERT retrieval followed by Qwen3 0.6B reranking. This is integration evidence only. It is not a default-promotion result because it depends on an explicit document fixture and a running retriever service; live mem0 indexing, service lifecycle, cold/warm latency monitoring, and rollback behavior still need separate proof.
