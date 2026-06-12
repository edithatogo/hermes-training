# ColBERT Service-Down Fallback Smoke - 2026-06-12

## Scope

This smoke verifies that `scripts/mem0_read.py --mode colbert --fallback-to-vector`
does not fail a read when the local `LiquidAI/LFM2-ColBERT-350M` retriever
service is not running.

The service on `http://127.0.0.1:8765` was intentionally stopped before the run.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_read_latency_probe.py \
  --mode colbert \
  --query "What is the active mem0 Qdrant collection?" \
  --iterations 1 \
  --run-id mem0-colbert-service-down-fallback-20260612 \
  --timeout-s 60 \
  --read-wall-timeout-s 90 \
  --subprocess-read \
  --fallback-to-vector \
  --cache-ttl-s 0
```

## Result

| Metric | Value |
|---|---:|
| Success count | 1 |
| Fallback count | 1 |
| Input count | 1 |
| Total latency p50 | 2.939s |
| mem0 search latency p50 | 2.925s |
| Rerank latency p50 | 0.000s |

Fallback reason:

```text
retriever service unavailable: [Errno 61] Connection refused
```

Raw output:

`/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-colbert-service-down-fallback-20260612`

## Decision

The opt-in ColBERT read mode has a safe service-down behavior when
`--fallback-to-vector` is enabled. It should remain opt-in until the service
lifecycle is managed by the wrapper or a supervisor.
