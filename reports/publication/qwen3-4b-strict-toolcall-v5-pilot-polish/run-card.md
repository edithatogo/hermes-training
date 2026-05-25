# Qwen3 4B Strict Tool-Call V5 Pilot Polish Run Card

Date: 2026-05-25

## Identity

- Candidate: `qwen3-4b-strict-toolcall-v5-pilot-polish`
- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter path:
  `gemma4/experiments/qwen3-4b-strict-toolcall-v5-pilot-polish/lora_adapter`
- Training config:
  `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v5-pilot-polish.yaml`
- Training data:
  `gemma4/data/strict_tool_call/expanded_splits_v5_pilot_polish`
- Runtime condition: `/no_think` plus assistant prefill
  `<think>\n\n</think>\n\n`

## Dataset

V5 starts from V4 targeted data and adds non-heldout strict-compatible
invalid-tool examples designed to improve unsupported-tool refusal behavior.

An earlier draft included ordinary instruction-following examples. The strict
tool-call audit rejected those rows because their assistant outputs were neither
tool calls nor refusals, so they were removed before training.

Dataset audits:

- Overlap audit:
  `reports/publication/qwen3-4b-strict-toolcall-v5-pilot-polish/dataset-overlap-audit.json`
- Token audit:
  `reports/publication/qwen3-4b-strict-toolcall-v5-pilot-polish/dataset-token-audit.json`

Token counts:

| Split | Rows | Tokens |
|---|---:|---:|
| train | 100 | 25,177 |
| val | 5 | 1,337 |
| valid | 5 | 1,337 |
| test | 5 | 1,314 |

## Training

Command:

```bash
cd gemma4
source ../scripts/env.sh
../.venv/bin/python scripts/train.py \
  --config scripts/train_config.qwen3-4b.strict-toolcall-v5-pilot-polish.yaml
```

Raw training log:

```text
/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v5-pilot-polish-train-20260525.log
```

Key metrics:

| Metric | Value |
|---|---:|
| Train rows | 100 |
| Valid rows | 5 |
| Iterations | 150 |
| Trained tokens | 37,867 |
| Best observed validation loss | 0.640 at iterations 110 and 120 |
| Final validation loss | 0.689 |
| Peak memory | 3.785 GB |
| Wall time | 273.1 s |

## Evaluation

All runs used `/no_think` plus assistant prefill
`<think>\n\n</think>\n\n`.

| Suite | Pass rate | Raw output root |
|---|---:|---|
| Held-out strict local tool-call | 0.875 | `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v5-pilot-polish-heldout-prefill-20260525` |
| Mirrored regression | 1.000 | `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v5-pilot-polish-mirrored-prefill-20260525` |
| BFCL-style pilot | 1.000 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-local-bfcl-prefill-20260525` |
| IFEval-style pilot | 0.667 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-local-ifeval-prefill-20260525` |
| Coding pilot | 1.000 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-local-coding-prefill-20260525` |

Held-out failure:

- `heldout-argument-correctness-lab-order`: generated valid tool-call JSON but
  extracted `priority` as `"priority"` instead of the requested value.

IFEval-style pilot failure:

- `ifeval-forbidden-word`: avoided the forbidden word, but missed the required
  phrase `completed successfully`.

## Decision

Do not promote or publish V5. It improved the BFCL-style pilot from V4's `0.667`
to `1.000`, but it regressed the strict held-out Hermes tool-call gate from
V4's `1.000` to `0.875`. V4 remains the recommended/public adapter.

Next experiment should pair invalid-tool polish with argument-extraction
retention examples and should evaluate earlier checkpoints before choosing a
final adapter.
