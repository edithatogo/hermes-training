# MLX BGE Broader Cold/Warm Latency Probe

Run ID: `mem0-read-mlx-bge-broader-cold-warm-20260613b`
Created: `2026-06-13T01:26:08.905441+00:00`

## Scope

This read-only probe tested the opt-in `mlx-bge` guarded mem0 read mode across
the five standard operational memory queries and two iterations. The first
iteration used a fresh SSD-backed cache path; the second iteration reused that
cache. Raw mem0 result text is not committed.

## Command Shape

```bash
source scripts/env.sh
HF_HUB_DISABLE_XET=1 ./.venv/bin/python scripts/run_mem0_read_latency_probe.py \
  --mode mlx-bge \
  --iterations 2 \
  --run-id mem0-read-mlx-bge-broader-cold-warm-20260613b \
  --output-dir /Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-mlx-bge-broader-cold-warm-20260613b \
  --cache-path /Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-mlx-bge-broader-cold-warm-20260613b/cache.json \
  --timeout-s 180 \
  --read-wall-timeout-s 90 \
  --subprocess-read \
  --cache-ttl-s 300 \
  --fallback-to-vector
```

## Result

| Metric | Value |
|---|---:|
| Cases | 10 |
| Query count | 5 |
| Iterations | 2 |
| Success count | 10 |
| Fallback count | 0 |
| mem0 cache hit count | 5 |
| Input count min / max | 1 / 1 |
| Multi-result count | 0 |
| Singleton count | 10 |
| Empty count | 0 |
| Total latency p50 | 5.996s |
| Total latency p95 | 8.544s |
| mem0 search latency p50 | 1.413s |
| mem0 search latency p95 | 3.997s |
| Rerank latency p50 | 0.048s |
| Rerank latency p95 | 0.050s |

## Cold vs Cache

| Scenario | Count | Total p50 | Total p95 | mem0 search p50 | Rerank p50 |
|---|---:|---:|---:|---:|---:|
| Cold | 5 | 7.404s | 9.058s | 2.856s | 0.050s |
| Cache hit | 5 | 4.552s | 4.800s | 0.000s | 0.048s |

Cache p50 speedup ratio: `1.6x`.

## Artifacts

- Private summary: `/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-mlx-bge-broader-cold-warm-20260613b/summary.json`
- Private results JSONL: `/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-mlx-bge-broader-cold-warm-20260613b/results.jsonl`
- Private generated markdown: `/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-mlx-bge-broader-cold-warm-20260613b/summary.md`

## Decision

Keep `mlx-bge` as an explicit opt-in read mode with vector fallback. The broader
probe is safe and repeatable, but the observed p50 still reflects child-process
model startup cost: cold reads were about `7.404s` p50 and cache-hit reads were
about `4.552s` p50. The live result sets were singleton-only, so this is not a
multi-result quality claim. This is acceptable for deliberate memory inspection and
Hermes tool use, but not for every-turn automatic prelude reads.
