# mem0 Cached Read Path Benchmark

Date: 2026-05-26

## Purpose

Benchmark opt-in cached `scripts/mem0_read.py` calls for repeated agent memory
reads without changing mem0 defaults.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_read_latency_probe.py \
  --mode close-margin \
  --iterations 2 \
  --run-id mem0-read-cache-close-margin-20260526 \
  --cache-path /Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-cache-close-margin-20260526/cache/mem0-read-cache.json \
  --cache-ttl-s 3600 \
  --timeout-s 180
```

## Result

Output:
`/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-cache-close-margin-20260526`

| Metric | Value |
|---|---:|
| Exit code | 0 |
| Cases | 10 |
| Success count | 10 |
| Fallback count | 0 |
| Cache hit count | 5 |
| Input count min / max | 1 / 1 |
| Singleton count | 10 |
| Multi-result count | 0 |
| Empty count | 0 |
| Cold total latency p50 | 2.904s |
| Cold total latency p95 | 2.915s |
| Cache-hit total latency p50 | 0.000s |
| Cache-hit total latency p95 | 0.000s |
| Cold mem0 search latency p50 | 2.903s |
| Cache-hit mem0 search latency p50 | 0.000s |

## Decision

The cached read path is suitable for explicit repeated memory reads when the
caller supplies a short TTL and refreshes after writes. It is not a default mem0
configuration change, and the singleton-only live-store result means this run is
latency evidence, not multi-result quality evidence.
