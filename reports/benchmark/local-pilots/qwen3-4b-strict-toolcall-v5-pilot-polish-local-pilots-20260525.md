# Qwen3 4B Strict Tool-Call V5 Pilot Polish Local Pilot Benchmarks

Date: 2026-05-25

## Identity

- Model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v5-pilot-polish/lora_adapter`
- Runtime: MLX native local generation
- Prompt profile: `/no_think` user prefix plus assistant prefill `<think>\n\n</think>\n\n`
- Artifact root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/`

These are repo-native pilot suites, not official BFCL, IFEval, or HumanEval
scores.

## Results

### Strict-Compatible Rerun

This rerun uses the corrected V5 data contract: V4 plus invalid-tool polish rows
only. Ordinary instruction-following rows were excluded before training because
they are outside the strict tool-call dataset contract.

| Checkpoint | Suite | Cases | Passed | Pass rate | Residual failure | Raw output root |
|---|---|---:|---:|---:|---|---|
| Final strict-compatible rerun | BFCL-style pilot | 3 | 3 | 1.000 | none | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-local-bfcl-prefill-20260525` |
| Final strict-compatible rerun | IFEval-style pilot | 3 | 2 | 0.667 | `ifeval-forbidden-word` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-local-ifeval-prefill-20260525` |
| Final strict-compatible rerun | Coding sanity pilot | 3 | 3 | 1.000 | none | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-local-coding-prefill-20260525` |

### Superseded Mixed-Draft Runs

The earlier mixed-draft run included ordinary instruction-following rows. It is
preserved here as superseded evidence because those rows were later rejected by
the strict dataset audit.

| Checkpoint | Suite | Cases | Passed | Pass rate | Residual failure | Raw output root |
|---|---|---:|---:|---:|---|---|
| Mixed draft final | BFCL-style pilot | 3 | 2 | 0.667 | `bfcl-invalid-tool` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-final-local-bfcl-prefill-20260525` |
| Mixed draft final | IFEval-style pilot | 3 | 3 | 1.000 | none | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-final-local-ifeval-prefill-20260525` |
| Mixed draft final | Coding sanity pilot | 3 | 2 | 0.667 | `coding-python-filter-even` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-final-local-coding-prefill-20260525` |
| Mixed draft iter 125 | BFCL-style pilot | 3 | 2 | 0.667 | `bfcl-invalid-tool` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter125-local-bfcl-prefill-20260525` |
| Mixed draft iter 125 | IFEval-style pilot | 3 | 3 | 1.000 | none | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter125-local-ifeval-prefill-20260525` |
| Mixed draft iter 125 | Coding sanity pilot | 3 | 2 | 0.667 | `coding-python-filter-even` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter125-local-coding-prefill-20260525` |
| Mixed draft iter 100 | BFCL-style pilot | 3 | 2 | 0.667 | `bfcl-invalid-tool` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter100-local-bfcl-prefill-20260525` |
| Mixed draft iter 100 | IFEval-style pilot | 3 | 3 | 1.000 | none | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter100-local-ifeval-prefill-20260525` |
| Mixed draft iter 100 | Coding sanity pilot | 3 | 2 | 0.667 | `coding-python-filter-even` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter100-local-coding-prefill-20260525` |

## Interpretation

The strict-compatible rerun fixes the V4 BFCL-style unsupported-tool pilot
failure, but it does not fix the IFEval-style wording failure. The superseded
mixed draft had the opposite shape: IFEval improved, but BFCL remained failed
and coding regressed.

Because the strict-compatible rerun also regressed the held-out publication
gate to `0.875`, all V5 variants remain evidence against promotion. Keep V4
targeted as the public adapter and treat V5 as a negative ablation.
