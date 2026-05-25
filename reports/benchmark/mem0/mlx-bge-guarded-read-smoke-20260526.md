# MLX BGE Guarded Read Smoke

Date: 2026-05-26

## Scope

Smoke the new explicit `mlx-bge` read mode after the 8-bit MLX BGE reranker
passed fixed, expanded, and isolated fixture gates. This is read-only and does
not modify the default mem0 configuration.

## Commands

```bash
HF_HUB_DISABLE_XET=1 ./.venv/bin/python scripts/mem0_read.py \
  "What is the active mem0 Qdrant collection?" \
  --mode mlx-bge \
  --timeout-s 180 \
  --cache-ttl-s 300 \
  --fallback-to-vector

HF_HUB_DISABLE_XET=1 ./.venv/bin/python scripts/hermes_mem0_tool.py \
  --query "What is the active mem0 Qdrant collection?" \
  --mode mlx-bge \
  --fallback-to-vector \
  --cache-ttl-s 300
```

## Result

| Path | ok | Cache hit | Input count | Total latency | Rerank latency |
|---|---:|---:|---:|---:|---:|
| `scripts/mem0_read.py` | true | false | 1 | 9.406s | 0.054s |
| `scripts/hermes_mem0_tool.py` | true | true | 1 | 4.939s | 0.067s |

Both outputs reported `read_only: true` and `mutates_mem0_config: false`.

## Decision

Keep `mlx-bge` as an explicit opt-in mode with vector fallback. It is now strong
enough for targeted daily-use latency probes, but the default mem0 path remains
`nomic-embed-text:latest`, `mem0_nomic_768`, and close-margin reads.
