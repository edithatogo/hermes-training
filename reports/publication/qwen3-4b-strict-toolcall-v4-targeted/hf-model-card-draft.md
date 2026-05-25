# Qwen3 4B Hermes Strict Tool-Call V4 Targeted

Draft status: not yet published.

## Summary

This is a LoRA adapter for `Qwen/Qwen3-4B-MLX-4bit` trained for strict local
Hermes-style tool-call output.

The adapter is intended for local evaluation and agent-runtime packaging. It
requires the recorded runtime prompt condition:

- first user turn prefixed with `/no_think`
- assistant prefill: `<think>\n\n</think>\n\n`

Without the assistant prefill, the model still emits an empty leading thinking
wrapper and does not satisfy the strict raw-output gate.

## Base Model

- Base: `Qwen/Qwen3-4B-MLX-4bit`
- Base license: Apache-2.0, checked via Hugging Face API on 2026-05-25

## Training

- Training config:
  `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v4-targeted.yaml`
- Data:
  `gemma4/data/strict_tool_call/expanded_splits_v4_targeted`
- Adapter:
  `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
- Training tokens: 37,936
- Dataset token audit: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-token-audit.json`
- Dataset overlap audit: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-overlap-audit.json`
- Peak memory: 3.785 GB

## Evaluation

Held-out strict local tool-call gate:

| Suite | Pass | JSON valid | Arguments | Invalid tool | Multi-turn |
|---|---:|---:|---:|---:|---:|
| `benchmarks/tool_call_local/heldout_suite.json` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Mirrored regression:

| Suite | Pass |
|---|---:|
| `benchmarks/tool_call_local/suite.json` | 1.000 |

Exact held-out command:

```bash
source scripts/env.sh
PYTHONPATH=scripts ./.venv/bin/python scripts/run_tool_call_benchmark.py \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --user-prefix /no_think \
  --assistant-prefill $'<think>\n\n</think>\n\n' \
  --run-id qwen3-4b-strict-toolcall-v4-targeted-heldout-prefill-20260525 \
  --max-tokens 256
```

Raw local artifact:

```text
/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v4-targeted-heldout-prefill-20260525
```

The reusable runtime prompt contract is recorded in
`RUNTIME_PROMPT_PROFILES.yaml` as `qwen3-no-think-assistant-prefill`.

## Limitations

- This is a small local strict-format benchmark, not broad BFCL or production
  tool-use evidence.
- The adapter is sensitive to runtime prompt formatting.
- The V4 training data has no held-out user-prompt overlap in the recorded
  audit, but it shares one generic held-out tool name, `notify_care_team`.
- Public publication is pending dataset/source redistribution review and human
  approval.
