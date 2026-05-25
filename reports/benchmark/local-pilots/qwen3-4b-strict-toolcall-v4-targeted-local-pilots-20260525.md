# Qwen3 4B Strict Tool-Call V4 Targeted Local Pilot Benchmarks

Date: 2026-05-25

## Identity

- Model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
- Runtime: MLX native local generation
- Prompt profile: `/no_think` user prefix plus assistant prefill `<think>\n\n</think>\n\n`
- Artifact root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/`

These are repo-native pilot suites, not official BFCL, IFEval, or HumanEval
scores. They are designed to give cheap local regression evidence before
spending cloud budget or publishing a model card.

## Commands

```bash
PYTHONPATH=scripts ./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --run-id qwen3-4b-strict-toolcall-v4-targeted-local-bfcl-prefill-20260525 \
  --user-prefix /no_think \
  --assistant-prefill $'<think>\n\n</think>\n\n'

PYTHONPATH=scripts ./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --suite benchmarks/endpoint_pilots/ifeval_pilot.json \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --run-id qwen3-4b-strict-toolcall-v4-targeted-local-ifeval-prefill-20260525 \
  --user-prefix /no_think \
  --assistant-prefill $'<think>\n\n</think>\n\n'

PYTHONPATH=scripts ./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --suite benchmarks/endpoint_pilots/coding_pilot.json \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --run-id qwen3-4b-strict-toolcall-v4-targeted-local-coding-prefill-20260525 \
  --user-prefix /no_think \
  --assistant-prefill $'<think>\n\n</think>\n\n'
```

## Results

| Suite | Cases | Passed | Pass rate | Raw output root |
|---|---:|---:|---:|---|
| BFCL-style pilot | 3 | 2 | 0.667 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-bfcl-prefill-20260525` |
| IFEval-style pilot | 3 | 2 | 0.667 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-ifeval-prefill-20260525` |
| Coding sanity pilot | 3 | 3 | 1.000 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-coding-prefill-20260525` |

## Failure Examples

- `bfcl-invalid-tool`: refused the unsupported action but echoed the forbidden
  tool name `delete_customer_record`, so the pilot exclusion check failed.
- `ifeval-forbidden-word`: avoided the forbidden word but did not include the
  required phrase `completed successfully`.

## Decision

The adapter remains publishable only as a local strict Hermes-agent candidate,
not as a broad benchmark winner. The local strict held-out gate is clean at
`1.000`, but the pilot results show remaining general instruction-following
and refusal-style polish work before any stronger public positioning.
