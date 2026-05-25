# MLX BGE Daily-Use Latency Probe

Date: 2026-05-26

## Scope

Run the first daily-use latency probe for the explicit `mlx-bge` guarded mem0
read mode. This mode uses
`flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit` as an MLX cross-encoder
reranker and keeps vector fallback enabled. It remains opt-in and does not
change `~/.mem0/config.json`, the `mem0_nomic_768` collection, or default
Hermes memory behavior.

## Commands

The first in-process probe entered Hugging Face artifact fetch/load and did not
complete within a practical daily-use window. It was manually terminated after
about seven minutes:

```bash
source scripts/env.sh
HF_HUB_DISABLE_XET=1 ./.venv/bin/python scripts/run_mem0_read_latency_probe.py \
  --mode mlx-bge \
  --query "What is the active mem0 Qdrant collection?" \
  --iterations 1 \
  --run-id mem0-read-mlx-bge-daily-use-20260526 \
  --timeout-s 180 \
  --cache-ttl-s 300 \
  --fallback-to-vector
```

The probe harness was then tightened to support child-process reads with a hard
wall timeout:

```bash
source scripts/env.sh
HF_HUB_DISABLE_XET=1 ./.venv/bin/python scripts/run_mem0_read_latency_probe.py \
  --mode mlx-bge \
  --query "What is the active mem0 Qdrant collection?" \
  --iterations 1 \
  --run-id mem0-read-mlx-bge-daily-use-subprocess-timeout-20260526 \
  --timeout-s 180 \
  --read-wall-timeout-s 60 \
  --subprocess-read \
  --cache-ttl-s 300 \
  --fallback-to-vector
```

## Result

| Metric | Value |
|---|---:|
| Cases | 1 |
| Success count | 1 |
| Cache hit count | 1 |
| Input count min / max | 1 / 1 |
| Total latency p50 | 4.610s |
| mem0 search latency p50 | 0.000s |
| Source mem0 search latency | 2.872s |
| Rerank latency p50 | 0.059s |
| Fallback count | 0 |

Artifacts:

- `/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-mlx-bge-daily-use-subprocess-timeout-20260526/summary.json`
- `/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-mlx-bge-daily-use-subprocess-timeout-20260526/results.jsonl`
- `/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-read-mlx-bge-daily-use-subprocess-timeout-20260526/summary.md`

## Decision

Keep `mlx-bge` as an explicit opt-in mode. The bounded child-process path makes
the daily-use probe safe to repeat, and the cached single-query result is usable,
but this is still not enough to promote MLX BGE into automatic/default mem0
reads. The next promotion gate is a multi-query cold/warm daily-use probe with
no artifact fetch stalls and acceptable p95 latency.
