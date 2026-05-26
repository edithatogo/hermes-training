# MLX lm-eval Direct Run: qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit10-20260526

Date: 2026-05-26T06:16:48.396698+00:00
Model: `Qwen/Qwen3-4B-MLX-4bit`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Tasks: `arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande`
Limit: `10`

## Result

| Field | Value |
|---|---|
| Status | scored |
| Output | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit10-20260526` |
| Load latency | 4.080s |
| Total latency | 200.854s |

## Metrics

| Task | Metric | Value |
|---|---|---:|
| `arc_challenge` | `acc,none` | 0.400000 |
| `arc_challenge` | `acc_norm,none` | 0.500000 |
| `hellaswag` | `acc,none` | 0.300000 |
| `hellaswag` | `acc_norm,none` | 0.600000 |
| `truthfulqa_mc2` | `acc,none` | 0.660350 |
| `gsm8k` | `exact_match,strict-match` | 0.700000 |
| `gsm8k` | `exact_match,flexible-extract` | 0.600000 |
| `winogrande` | `acc,none` | 0.700000 |
