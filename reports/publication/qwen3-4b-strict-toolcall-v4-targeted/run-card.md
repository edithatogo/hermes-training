# Qwen3 4B Strict Tool-Call V4 Targeted Run Card

## Identity

- Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Base license: Apache-2.0, verified via Hugging Face API on 2026-05-25
- Adapter path: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
- Training config: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v4-targeted.yaml`
- Training data: `gemma4/data/strict_tool_call/expanded_splits_v4_targeted`
- Runtime condition: Qwen `/no_think` user prefix plus assistant prefill `<think>\n\n</think>\n\n`

## Change

V4 starts from the V3 no-think strict tool-call data and adds targeted,
non-heldout examples for two residual failure families:

- exact extraction of short `message` argument text, using non-heldout examples
  such as `scan is ready for review`, `refill is ready for pickup`, and
  `transfer is ready for review`
- nested arrays of objects followed by trailing required fields

The held-out suite IDs, user prompts, entity values, and exact expected message
strings were not added to the V4 training rows. The overlap audit found one
shared generic tool name, `notify_care_team`; this is recorded below and remains
part of the publication review rather than being hidden.

## Training

Command:

```bash
cd gemma4
source ../scripts/env.sh
../.venv/bin/python scripts/train.py \
  --config scripts/train_config.qwen3-4b.strict-toolcall-v4-targeted.yaml
```

Training log:

```text
/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v4-targeted-train-20260525.log
```

Key metrics:

| Metric | Value |
|---|---:|
| Train rows | 92 |
| Valid rows | 5 |
| Iterations | 140 |
| Trained tokens | 37,936 |
| Best observed validation loss | 0.643 at iter 100 |
| Final validation loss | 0.709 |
| Peak memory | 3.785 GB |
| Wall time | 234.0 s |

Dataset audit:

```bash
./.venv/bin/python scripts/audit_tool_call_data.py \
  gemma4/data/strict_tool_call/expanded_splits_v4_targeted \
  --benchmark-suite benchmarks/tool_call_local/suite.json \
  --heldout-suite benchmarks/tool_call_local/heldout_suite.json \
  --max-errors 100 \
  > reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-overlap-audit.json
```

Result: valid JSONL structure, `107` rows, no held-out user-prompt overlap, one
held-out tool-name overlap (`notify_care_team`). The recorded audit is
`reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-overlap-audit.json`.

Token audit:

```bash
./.venv/bin/python scripts/dataset_token_audit.py \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --local-files-only \
  --data gemma4/data/strict_tool_call/expanded_splits_v4_targeted \
  --splits train val valid test \
  --output reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-token-audit.json
```

Result: train `24,331` tokens across `92` rows; val `1,337`, valid `1,337`,
test `1,314`.

## Strict Held-Out Gate

Command:

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

Result:

| Metric | Value |
|---|---:|
| Strict pass rate | 1.000 |
| JSON validity | 1.000 |
| Argument correctness | 1.000 |
| Invalid-tool handling | 1.000 |
| Multi-turn repair | 1.000 |
| Empty-think prefix cases | 0 / 8 |
| Strict failures rescued by stripping | 0 |
| Residual strict failures | 0 |

Raw output:

```text
/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v4-targeted-heldout-prefill-20260525
```

## Mirrored Regression

Command:

```bash
source scripts/env.sh
PYTHONPATH=scripts ./.venv/bin/python scripts/run_tool_call_benchmark.py \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --suite benchmarks/tool_call_local/suite.json \
  --user-prefix /no_think \
  --assistant-prefill $'<think>\n\n</think>\n\n' \
  --run-id qwen3-4b-strict-toolcall-v4-targeted-mirrored-prefill-20260525 \
  --max-tokens 256
```

Result: strict pass rate `1.000` across 6 mirrored cases.

Raw output:

```text
/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v4-targeted-mirrored-prefill-20260525
```

## Local Pilot Benchmarks

Report:

```text
reports/benchmark/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-pilots-20260525.md
```

Results:

| Suite | Pass rate | Raw output root |
|---|---:|---|
| BFCL-style pilot | 0.667 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-bfcl-prefill-20260525` |
| IFEval-style pilot | 0.667 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-ifeval-prefill-20260525` |
| Coding sanity pilot | 1.000 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-coding-prefill-20260525` |

These are repo-native pilot suites, not official BFCL, IFEval, or HumanEval
scores. Residual failures are documented in the report and should be treated
as the next improvement targets before making broad public benchmark claims.

## Important Limitation

Without assistant prefill, the same adapter still emits the Qwen empty thinking
wrapper and strict raw pass remains `0.250`, although diagnostic empty-think
stripping reaches `1.000`.

No model-card or runtime claim should omit the required assistant prefill.
The reusable prompt contract is recorded in
`RUNTIME_PROMPT_PROFILES.yaml` as `qwen3-no-think-assistant-prefill`.
