# MLX lm-eval Direct Run: qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-smoke-20260526

Date: 2026-05-26T06:17:15.392477+00:00
Model: `Qwen/Qwen3-4B-MLX-4bit`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Tasks: `arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande`
Limit: `1`

## Result

| Field | Value |
|---|---|
| Status | scored |
| Output | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-smoke-20260526` |
| Load latency | 1.607s |
| Total latency | 66.865s |

## Metrics

| Task | Metric | Value |
|---|---|---:|
| `arc_challenge` | `acc,none` | 1.000000 |
| `arc_challenge` | `acc_norm,none` | 1.000000 |
| `hellaswag` | `acc,none` | 0.000000 |
| `hellaswag` | `acc_norm,none` | 1.000000 |
| `truthfulqa_mc2` | `acc,none` | 0.004880 |
| `gsm8k` | `exact_match,strict-match` | 1.000000 |
| `gsm8k` | `exact_match,flexible-extract` | 0.000000 |
| `winogrande` | `acc,none` | 1.000000 |
