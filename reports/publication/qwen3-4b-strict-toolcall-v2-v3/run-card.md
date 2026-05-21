# Run Card: Qwen3 4B Strict Tool-Call V2/V3

Date: 2026-05-22

## Scope

This records two local MLX LoRA attempts for strict Hermes tool-call behavior on `Qwen/Qwen3-4B-MLX-4bit`.

- V2 adds explicit format-guard examples that forbid `<think>` and `</think>` wrappers.
- V3 duplicates V2 training rows with `/no_think` prefixed to the first user turn.
- Strict benchmark scoring was not changed.

## Training

| Attempt | Config | Data | Iterations | Trained Tokens | Peak Memory |
|---|---|---|---:|---:|---:|
| V2 | `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v2.yaml` | `gemma4/data/strict_tool_call/expanded_splits_v2` | 140 | 35,831 | 3.785 GB |
| V3 | `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v3-no-think.yaml` | `gemma4/data/strict_tool_call/expanded_splits_v3_no_think` | 120 | 31,208 | 3.785 GB |

Training artifacts are generated-only and remain outside Git under `gemma4/experiments/`.

## Benchmark Summary

| Attempt | Suite | Strict Pass | Diagnostic Empty-Think-Stripped Pass | Decision |
|---|---|---:|---:|---|
| V2 | held-out | 0.250 | 0.625 | blocked |
| V3 | mirrored | 0.167 | 1.000 | non-heldout regression only |
| V3 | held-out | 0.250 | 0.875 | blocked |
| V3 iter80 | held-out | 0.250 | 0.875 | blocked |

Raw outputs:

- `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v2-heldout-nothink-20260522`
- `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v3-nothink-mirrored-20260522`
- `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v3-nothink-heldout-20260522`
- `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v3-nothink-iter80-heldout-20260522`

## Decision

Do not publish the V2 or V3 adapters to Hugging Face. The held-out strict gate remains `1.000`; both attempts reached only `0.250` strict pass. V3 is useful as runtime-integration evidence because empty-think stripping recovers `0.875`, but that diagnostic score is not publication evidence.

Next work should prioritize a base/runtime that obeys no-thinking mode strictly, or a Hermes runtime normalization layer that removes empty Qwen thinking wrappers before downstream tool parsing.
