---
license: apache-2.0
base_model: Qwen/Qwen3-4B-MLX-4bit
tags:
- mlx
- lora
- qwen3
- tool-calling
- hermes-agent
- experimental
library_name: mlx
---

# Qwen3 4B Hermes Strict Tool-Call V6 Free-Text Copy

Release status: draft; public release pending approval.

## Summary

This draft describes a LoRA adapter for `Qwen/Qwen3-4B-MLX-4bit` trained for
strict local Hermes-style tool-call output. The selected checkpoint is
iteration 125 from the v6 free-text-copy run.

The adapter is intended for local Hermes agent runtime packaging and exact
tool-call argument extraction. It requires the recorded runtime prompt
condition:

- first user turn prefixed with `/no_think`
- assistant prefill: `<think>\n\n</think>\n\n`

## Training

- Training config:
  `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v6-free-text-copy.yaml`
- Training data:
  `gemma4/data/strict_tool_call/expanded_splits_v6_free_text_copy`
- Selected adapter:
  `gemma4/experiments/qwen3-4b-strict-toolcall-v6-free-text-copy/lora_adapter_iter125`
- Training tokens processed by final run: `43,724`
- Peak memory: `3.785 GB`

## Evaluation

Held-out strict local tool-call gate:

| Suite | Pass | JSON valid | Arguments | Invalid tool | Multi-turn |
|---|---:|---:|---:|---:|---:|
| `benchmarks/tool_call_local/heldout_suite.json` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Mirrored regression:

| Suite | Pass |
|---|---:|
| `benchmarks/tool_call_local/suite.json` | 1.000 |

Repo-native pilot benchmarks:

| Pilot | Pass | Notes |
|---|---:|---|
| BFCL-style pilot | 0.667 | local pilot only, not official BFCL |
| IFEval-style pilot | 0.667 | local pilot only, not official IFEval |
| Coding sanity pilot | 0.667 | local pilot only, not HumanEval/MBPP/EvalPlus |

This model card does not claim official BFCL, official IFEval, HumanEval,
MBPP, EvalPlus, BigCodeBench, LiveCodeBench, safety/refusal, RULER, or
long-context benchmark coverage. Current benchmark support is pilot-only
outside the local strict Hermes tool-call suites.

## Limitations

- Narrow strict tool-call adapter; not a broad chat or coding model release.
- Requires the documented runtime prompt profile.
- Pilot failures remain for unsupported-tool wording, code-filter formatting,
  and one instruction-following wording case.
- Public release remains blocked until explicit approval is recorded.
