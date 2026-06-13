# Qwen3 4B Strict Tool-Call V6 Free-Text Copy Run Card

Date: 2026-06-13

## Identity

- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter candidate: `gemma4/experiments/qwen3-4b-strict-toolcall-v6-free-text-copy/lora_adapter_iter125`
- Training config: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v6-free-text-copy.yaml`
- Training data: `gemma4/data/strict_tool_call/expanded_splits_v6_free_text_copy`
- Runtime condition: `/no_think` first-user prefix plus assistant prefill `<think>\n\n</think>\n\n`

## Training

- Train rows: `116`
- Validation rows: `5`
- Total iterations run: `170`
- Selected checkpoint: `125`
- Trained tokens at final iteration: `43,724`
- Best observed validation loss: `0.636` at iteration `110`
- Final validation loss: `0.670`
- Peak memory: `3.785 GB`
- Wall time: `241.9 s`
- Training log:
  `/Volumes/PortableSSD/hermes-evals/training/qwen3-4b-strict-toolcall-v6-free-text-copy-20260613.log`

Iteration 125 is selected because it passes both strict held-out and mirrored
benchmark suites. The final 170-iteration adapter is rejected because it
regresses to `0.875` on the held-out strict gate.

## Evaluation

| Checkpoint | Suite | Cases | Passed | Pass rate |
|---|---|---:|---:|---:|
| Iter 125 | Held-out strict local tool-call | 8 | 8 | `1.000` |
| Iter 125 | Mirrored regression | 6 | 6 | `1.000` |
| Iter 125 | BFCL-style pilot | 3 | 2 | `0.667` |
| Iter 125 | Coding sanity pilot | 3 | 2 | `0.667` |
| Iter 125 | IFEval-style pilot | 3 | 2 | `0.667` |

Raw evidence roots:

- `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v6-free-text-copy-iter125-heldout-prefill-20260613`
- `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v6-free-text-copy-iter125-mirrored-prefill-20260613`
- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v6-free-text-copy-iter125-local-bfcl-prefill-20260613`
- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v6-free-text-copy-iter125-local-coding-prefill-20260613`
- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v6-free-text-copy-iter125-local-ifeval-prefill-20260613`

## Publication Posture

This is locally ready as a strict Hermes tool-call candidate. Public adapter
publication remains blocked until the model card, release decision, and human
approval are finalized.
