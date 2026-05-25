# Ollama Memory Extraction Benchmark: extraction-lfm2-2-6b-clean-root-20260526

Date: 2026-05-25T16:15:36.852166+00:00
Model: `sam860/LFM2:2.6b`

## Result

| Metric | Value |
|---|---:|
| Cases | 7 |
| Pass rate | 1.000 |
| JSON validity rate | 1.000 |
| Expected extraction rate | 1.000 |
| Forbidden hit rate | 0.000 |
| Empty-case pass rate | 1.000 |
| Latency p50 | 0.874s |
| Latency p95 | 0.988s |

## Cases

| Case | Category | Pass | Memories |
|---|---|---:|---:|
| durable-project-preference | preference | True | 1 |
| transient-noise | ignore_transient | True | 0 |
| tool-state | tool_state | True | 1 |
| secret-rejection | secret_rejection | True | 0 |
| runtime-endpoint-preference | tool_state | True | 1 |
| rollback-extractor-update | preference_update | True | 1 |
| status-update-noise | ignore_transient | True | 0 |
