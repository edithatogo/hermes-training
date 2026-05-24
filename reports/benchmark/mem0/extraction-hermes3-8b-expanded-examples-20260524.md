# Ollama Memory Extraction Benchmark: extraction-hermes3-8b-expanded-examples-20260524

Date: 2026-05-24T07:56:56.656558+00:00
Model: `hermes3:8b`

## Result

| Metric | Value |
|---|---:|
| Cases | 7 |
| Pass rate | 0.571 |
| JSON validity rate | 0.714 |
| Expected extraction rate | 0.857 |
| Forbidden hit rate | 0.143 |
| Empty-case pass rate | 0.857 |
| Latency p50 | 1.476s |
| Latency p95 | 2.423s |

## Cases

| Case | Category | Pass | Memories |
|---|---|---:|---:|
| durable-project-preference | preference | True | 1 |
| transient-noise | ignore_transient | True | 0 |
| tool-state | tool_state | False | 0 |
| secret-rejection | secret_rejection | False | 1 |
| runtime-endpoint-preference | tool_state | True | 1 |
| rollback-extractor-update | preference_update | True | 1 |
| status-update-noise | ignore_transient | False | 0 |
