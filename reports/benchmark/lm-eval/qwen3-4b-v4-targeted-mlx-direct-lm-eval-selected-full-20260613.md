# MLX lm-eval Direct Run: qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613

Date: 2026-06-13T01:43:44.824368+00:00
Last update: 2026-06-13T02:00:33.000000+00:00
Model: `Qwen/Qwen3-4B-MLX-4bit`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Tasks: `arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande`
Limit: `full`

## Result

| Field | Value |
|---|---|
| Status | blocked |
| Output | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613` |
| Load latency | 3.474s |
| Total latency | 731.827s |

## Error

```text
KeyboardInterrupt: local no-limit MLX full scorecard was manually stopped after 731.827s with 0/5 tasks completed; route full selected-task scorecard to Colab/Azure/offload lane or resume explicitly.
```

| Progress | Value |
|---|---|
| Completed tasks | `0/5` |
| Current task | `arc_challenge` |
| Pending tasks | `arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande` |

## Decision

This is not a benchmark scorecard and must not be used for model comparison.
The local M1 Max direct-MLX no-limit path did not complete the first selected
task after 731.827 seconds, so the full scorecard should move to the Colab,
Azure, or other offload lane unless explicitly resumed for a long local run.
