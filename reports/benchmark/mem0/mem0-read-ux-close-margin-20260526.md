# mem0 Read UX Latency Probe

Date: 2026-05-26

## Purpose

Measure `scripts/mem0_read.py` as an agent-facing read-only memory lookup path
before wiring it into Hermes runtime.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_read_latency_probe.py \
  --mode close-margin \
  --iterations 1 \
  --run-id mem0-read-ux-close-margin-20260526 \
  --timeout-s 180
```

## Result

Output:
`/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-ux-close-margin-20260526`

| Metric | Value |
|---|---:|
| Exit code | 0 |
| Query count | 5 |
| Success count | 5 |
| Fallback count | 0 |
| Input count min / max | 1 / 1 |
| Singleton count | 5 |
| Multi-result count | 0 |
| Empty count | 0 |
| Total latency p50 | 4.926s |
| Total latency p95 | 4.940s |
| Total latency mean | 4.517s |
| mem0 search latency p50 | 4.926s |
| mem0 search latency p95 | 4.940s |
| Rerank latency p50 | 0.000s |

## Decision

The guarded read wrapper is acceptable as an explicit agent tool, but not yet as
an always-on automatic prelude for every Hermes turn. The bottleneck is the live
`mem0 cmd search` call, not close-margin reranking. Wire it only behind
intentional memory-read calls or cache/batch it before using it in every agent
step.

Quality evidence remains the isolated fixture: close-margin passed the
multi-result recency gate at `1.000`, while Qwen3 0.6B matched vector at
`0.667`. This UX probe was singleton-only and should not be used as a
multi-result quality claim.
