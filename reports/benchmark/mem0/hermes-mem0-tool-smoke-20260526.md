# Hermes mem0 Tool Smoke

Date: 2026-05-26

## Purpose

Validate `scripts/hermes_mem0_tool.py` as the explicit command contract for
Hermes-agent memory reads.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/hermes_mem0_tool.py \
  --query "What is the active mem0 Qdrant collection?" \
  --cache-path /Volumes/PortableSSD/hermes-evals/hermes-mem0-tool/hermes-mem0-tool-smoke-20260526/cache.json \
  --cache-ttl-s 300 \
  --timeout-s 120
```

The command was run twice with the same cache path.

## Result

| Metric | First read | Second read |
|---|---:|---:|
| Exit code | 0 | 0 |
| `ok` | true | true |
| Read-only | true | true |
| Mutates mem0 config | false | false |
| Input count | 1 | 1 |
| Cache hit | false | true |
| Total latency | 3.999s | 0.000s |
| mem0 search latency | 3.998s | 0.000s |
| Rerank latency | 0.000s | 0.000s |

## Decision

The command wrapper is suitable as an explicit Hermes-agent memory-read tool.
Keep it out of the automatic turn prelude; callers should set a short cache TTL
and refresh after writes or store changes.
