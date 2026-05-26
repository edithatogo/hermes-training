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

# Qwen3 4B Hermes Strict Tool-Call V4 Targeted

Release status: public experimental adapter release.

## Summary

This is a LoRA adapter for `Qwen/Qwen3-4B-MLX-4bit` trained for strict local
Hermes-style tool-call output.

Adapter repo: `https://huggingface.co/edithatogo/qwen3-4b-hermes-lora`

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

Repo-native pilot benchmarks:

| Pilot | Pass | Notes |
|---|---:|---|
| BFCL-style pilot | 0.667 | local pilot only, not official BFCL |
| IFEval-style pilot | 0.667 | local pilot only, not official IFEval |
| Coding sanity pilot | 1.000 | local pilot only, not HumanEval/MBPP |

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
- The release does not include official BFCL, HumanEval, MBPP, EvalPlus,
  BigCodeBench, LiveCodeBench, safety/refusal, or RULER long-context scores.
- The selected `lm_eval` endpoint route was attempted separately, but the current
  local MLX endpoint is not loglikelihood-compatible for those tasks. A direct
  MLX adapter has scored bounded selected-task limit-10 and limit-25 runs; treat
  those as pilot evidence only, not as full official `lm_eval` or leaderboard
  scores.
- The adapter is sensitive to runtime prompt formatting.
- The V4 training data has no held-out user-prompt overlap in the recorded
  audit, but it shares one generic held-out tool name, `notify_care_team`.
- Dataset/source redistribution review is complete for adapter-release purposes
  with caveats; public dataset publication remains separate and blocked pending
  scope approval.
- Public release approval is recorded in `release-decision.md`; the publication
  bundle is expected to pass `scripts/validate_publication_bundle.py
  --require-ready`.
