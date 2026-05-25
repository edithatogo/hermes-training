# Qwen3 4B Strict Tool-Call V5 Pilot Polish Run Card

## Identity

- Candidate: `qwen3-4b-strict-toolcall-v5-pilot-polish`
- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter path: `gemma4/experiments/qwen3-4b-strict-toolcall-v5-pilot-polish/lora_adapter`
- Training config: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v5-pilot-polish.yaml`
- Training data: `gemma4/data/strict_tool_call/expanded_splits_v5_pilot_polish`
- Runtime condition: Qwen `/no_think` user prefix plus assistant prefill `<think>\n\n</think>\n\n`
- Decision: NOT PROMOTED. Keep public adapter on V4 targeted.

## Change

V5 starts from `expanded_splits_v4_targeted` and adds targeted pilot-polish rows
for three behaviors:

- refusing unavailable tools without echoing the unavailable tool name
- satisfying wording constraints while preserving required phrases such as
  `runtime smoke passed`
- retaining a positive valid tool-call example alongside the refusal examples

Each new prompt also has a `/no_think` variant. The added rows intentionally do
not use held-out strict suite prompts or held-out entity values.

## Training

Command:

```bash
cd gemma4
source ../scripts/env.sh
../.venv/bin/python scripts/train.py \
  --config scripts/train_config.qwen3-4b.strict-toolcall-v5-pilot-polish.yaml
```

Training log:

```text
/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v5-pilot-polish-train-20260525.log
```

Key metrics:

| Metric | Value |
|---|---:|
| Train rows | 100 |
| Valid rows | 5 |
| Iterations | 150 |
| Trained tokens | 35,969 |
| Best observed validation loss | 0.638 at iter 130 |
| Final validation loss | 0.680 |
| Peak memory | 3.785 GB |
| Wall time | 294.6 s |

Dataset audit:

```text
reports/publication/qwen3-4b-strict-toolcall-v5-pilot-polish/dataset-overlap-audit.json
```

Result: valid JSONL structure, `115` rows including the `valid` alias, `110`
unique IDs, no held-out user-prompt overlap, and one held-out generic tool-name
overlap: `notify_care_team`.

Token audit:

```text
reports/publication/qwen3-4b-strict-toolcall-v5-pilot-polish/dataset-token-audit.json
```

Result: train `25,177` tokens across `100` rows; val `1,337`, valid `1,337`,
test `1,314`.

## Strict Held-Out Gate

All runs used:

```text
--suite benchmarks/tool_call_local/heldout_suite.json
--user-prefix /no_think
--assistant-prefill <think>\n\n</think>\n\n
```

| Adapter checkpoint | Strict pass rate | Passed | Residual failures | Raw output root |
|---|---:|---:|---|---|
| Final | 0.750 | 6 / 8 | `heldout-argument-correctness-lab-order`, `heldout-multi-turn-repair-weather-alert` | `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v5-pilot-polish-heldout-prefill-20260525` |
| Iter 125 | 0.875 | 7 / 8 | `heldout-argument-correctness-lab-order` | `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v5-pilot-polish-iter125-heldout-prefill-20260525` |
| Iter 100 | 0.875 | 7 / 8 | `heldout-argument-correctness-lab-order` | `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v5-pilot-polish-iter100-heldout-prefill-20260525` |
| Iter 75 | 0.750 | 6 / 8 | `heldout-argument-correctness-lab-order`, `heldout-multi-turn-repair-purchase-order` | `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v5-pilot-polish-iter75-heldout-prefill-20260525` |
| Iter 50 | 0.125 | 1 / 8 | 7 residual failures | `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v5-pilot-polish-iter50-heldout-prefill-20260525` |
| Iter 25 | 0.375 | 3 / 8 | 5 residual failures | `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v5-pilot-polish-iter25-heldout-prefill-20260525` |

V5 does not meet the strict publication gate. V4 targeted remains the current
public adapter because it passed the same strict held-out gate at `1.000` under
the same runtime condition.

## Local Pilot Benchmarks

Report:

```text
reports/benchmark/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-local-pilots-20260525.md
```

Results:

| Checkpoint | BFCL-style pilot | IFEval-style pilot | Coding sanity pilot |
|---|---:|---:|---:|
| Final | 0.667 | 1.000 | 0.667 |
| Iter 125 | 0.667 | 1.000 | 0.667 |
| Iter 100 | 0.667 | 1.000 | 0.667 |

The IFEval-style failure from V4 is fixed, but the BFCL-style invalid-tool
failure remains and the coding pilot regresses from `1.000` on V4 to `0.667`.

## Decision

Do not publish or upload V5 to Hugging Face. It is a useful negative result:
the pilot-polish rows improved narrow instruction-following behavior but
damaged strict held-out tool-call behavior and coding sanity. Continue public
release documentation and model-card claims from V4 targeted only.

Next experiments should avoid replacing the strict adapter with mixed
instruction-polish data. Safer options are:

- keep V4 as the strict tool-call adapter and handle unsupported-tool wording at
  runtime
- train a separate tiny instruction-polish adapter and compare adapter stacking
  or routing
- continue from V4 with a much smaller no-heldout refusal-only ablation before
  adding any coding or general instruction rows
