# Ollama Memory Extraction Benchmark: extraction-lfm2-2-6b-prompt-file-20260524

Date: 2026-05-24T08:28:46.259951+00:00
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
| Latency p50 | 0.866s |
| Latency p95 | 2.982s |

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
