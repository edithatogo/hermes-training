# MLX lm-eval Direct Run: qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit25-20260526

Date: 2026-05-26T06:52:58.040857+00:00
Model: `Qwen/Qwen3-4B-MLX-4bit`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Tasks: `arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande`
Limit: `25`

## Result

| Field | Value |
|---|---|
| Status | scored |
| Output | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit25-20260526` |
| Load latency | 3.509s |
| Total latency | 363.589s |

## Metrics

| Task | Metric | Value |
|---|---|---:|
| `arc_challenge` | `acc,none` | 0.440000 |
| `arc_challenge` | `acc_norm,none` | 0.560000 |
| `hellaswag` | `acc,none` | 0.520000 |
| `hellaswag` | `acc_norm,none` | 0.720000 |
| `truthfulqa_mc2` | `acc,none` | 0.646196 |
| `gsm8k` | `exact_match,strict-match` | 0.560000 |
| `gsm8k` | `exact_match,flexible-extract` | 0.560000 |
| `winogrande` | `acc,none` | 0.600000 |
