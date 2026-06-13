# Scorecard Offload Readiness: qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613

Date: 2026-06-13T02:00:47.025697+00:00
Status: `blocked`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Model: `Qwen/Qwen3-4B-MLX-4bit`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Adapter framework: `mlx-native`
Exact adapter portable: `false`

## Blockers

- adapter is MLX-native; CUDA Colab/Azure cannot load it through standard Transformers/PEFT

## Next Actions

- export or convert the MLX LoRA to a Hugging Face PEFT adapter with equivalent behavior
- or run the full scorecard on Apple Silicon with an explicit long-runtime window
- or benchmark only the base model/another portable candidate and label it separately

## Claim Boundary

No cloud scorecard claim until the exact adapter is portable or the report explicitly labels a different model.
