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

| Checkpoint | Suite | Cases | Passed | Pass rate | Residual failure | Raw output root |
|---|---|---:|---:|---:|---|---|
| Final | BFCL-style pilot | 3 | 2 | 0.667 | `bfcl-invalid-tool` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-final-local-bfcl-prefill-20260525` |
| Final | IFEval-style pilot | 3 | 3 | 1.000 | none | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-final-local-ifeval-prefill-20260525` |
| Final | Coding sanity pilot | 3 | 2 | 0.667 | `coding-python-filter-even` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-final-local-coding-prefill-20260525` |
| Iter 125 | BFCL-style pilot | 3 | 2 | 0.667 | `bfcl-invalid-tool` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter125-local-bfcl-prefill-20260525` |
| Iter 125 | IFEval-style pilot | 3 | 3 | 1.000 | none | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter125-local-ifeval-prefill-20260525` |
| Iter 125 | Coding sanity pilot | 3 | 2 | 0.667 | `coding-python-filter-even` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter125-local-coding-prefill-20260525` |
| Iter 100 | BFCL-style pilot | 3 | 2 | 0.667 | `bfcl-invalid-tool` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter100-local-bfcl-prefill-20260525` |
| Iter 100 | IFEval-style pilot | 3 | 3 | 1.000 | none | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter100-local-ifeval-prefill-20260525` |
| Iter 100 | Coding sanity pilot | 3 | 2 | 0.667 | `coding-python-filter-even` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-iter100-local-coding-prefill-20260525` |

## Interpretation

V5 fixes the V4 IFEval-style wording failure, but it does not fix the
unsupported-tool BFCL-style failure. It also regresses the coding sanity pilot
from V4's `1.000` to `0.667`.

Because the strict held-out gate also regressed below `1.000`, these pilot
results are recorded as evidence against promoting V5. Keep V4 targeted as the
public adapter and treat V5 as a negative ablation.
