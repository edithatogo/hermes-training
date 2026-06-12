# ColBERT Read Stack Smoke - 2026-06-12

## Scope

This smoke controls the local `LiquidAI/LFM2-ColBERT-350M` service lifecycle,
runs the opt-in `mem0_read.py --mode colbert` wrapper while the service is
healthy, then stops the service and verifies `--fallback-to-vector` behavior.

## Service

- URL: `http://127.0.0.1:8765`
- Model: `LiquidAI/LFM2-ColBERT-350M`
- Device: `mps`
- Local files only: `True`

## Service-Up Probe

| Metric | Value |
|---|---:|
| Success count | 2 |
| Fallback count | 0 |
| Multi-result count | 0 |
| Singleton count | 2 |
| Empty count | 0 |
| Total latency p50 | 3.099s |
| mem0 search latency p50 | 2.861s |
| Retriever latency p50 | 0.238s |

Raw output: `/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-colbert-stack-20260612-service-up`

## Service-Down Fallback Probe

| Metric | Value |
|---|---:|
| Success count | 1 |
| Fallback count | 1 |
| Total latency p50 | 2.898s |
| mem0 search latency p50 | 2.885s |

Raw output: `/Volumes/PortableSSD/hermes-evals/mem0-read-latency/mem0-colbert-stack-20260612-service-down-fallback`

## Decision Use

Use this report to decide whether the live ColBERT path has enough
multi-candidate coverage and service lifecycle proof to become the default
Hermes mem0 read path. If the service-up probe has only singleton results,
the stack remains opt-in even when fallback is healthy.
