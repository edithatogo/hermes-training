# MLX lm-eval Direct Run: qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-seq-20260610

Date: 2026-06-10T09:11:28.913857+00:00
Last update: 2026-06-11T07:27:09.969756+00:00
Model: `Qwen/Qwen3-4B-MLX-4bit`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Tasks: `arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande`
Limit: `full`

## Result

| Field | Value |
|---|---|
| Status | partial-interrupted |
| Output | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-seq-20260610` |
| Load latency | 3.844s |
| Total latency | 80141.056s |

| Progress | Value |
|---|---|
| Completed tasks | `1/5` |
| Interrupted task | `hellaswag` |
| Pending tasks | `hellaswag,truthfulqa_mc2,gsm8k,winogrande` |

## Decision

This is partial evidence only. The process is no longer active and only
`arc_challenge` completed. Do not use this report as a full `lm-eval-selected`
candidate scorecard or leaderboard-style result.

## Metrics

| Task | Metric | Value |
|---|---|---:|
| `arc_challenge` | `acc,none` | 0.492321 |
| `arc_challenge` | `acc_norm,none` | 0.520478 |
