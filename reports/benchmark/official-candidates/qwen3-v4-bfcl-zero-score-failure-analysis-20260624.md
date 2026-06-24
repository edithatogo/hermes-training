# Qwen3 v4 BFCL Zero-Score Failure Analysis

- Status: `blocked-clean-regeneration-required`
- Result root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/results/Qwen_Qwen3-4B-Instruct-2507-FC/non_live`
- Total rows: 800
- Upstream errors: 796
- Blank outputs: 4
- Tool-call-like outputs: 0
- Contaminated rows: 800 (100.00%)

## Category Counts

| Category | Rows | Upstream errors | Blank outputs | Tool-call-like | Other completed |
| --- | ---: | ---: | ---: | ---: | ---: |
| multiple | 200 | 196 | 4 | 0 | 0 |
| parallel | 200 | 200 | 0 | 0 | 0 |
| simple_python | 400 | 400 | 0 | 0 | 0 |

## Gate

This artifact is not promotable as model-quality evidence. Regenerate BFCL outputs cleanly before treating the selected-slice score as meaningful.

Required rerun contract:
- Start a fresh OpenAI-compatible endpoint and keep it reachable for the entire run.
- Write to a new BFCL output root or pass --allow-overwrite after archiving stale artifacts.
- Use low concurrency first, e.g. --num-threads 1, to avoid local proxy overload.
- Preserve endpoint/proxy logs with the score artifact.
- Only promote BFCL evidence when upstream_error_rows == 0 and blank_output_rows == 0.
