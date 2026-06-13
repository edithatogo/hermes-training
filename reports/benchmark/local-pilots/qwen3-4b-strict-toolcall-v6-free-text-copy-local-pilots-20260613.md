# Qwen3 4B Strict Tool-Call V6 Free-Text Copy Local Benchmarks

Date: 2026-06-13

## Identity

- Model: `Qwen/Qwen3-4B-MLX-4bit`
- Recommended adapter checkpoint:
  `gemma4/experiments/qwen3-4b-strict-toolcall-v6-free-text-copy/lora_adapter_iter125`
- Runtime: MLX native local generation
- Prompt profile: `/no_think` user prefix plus assistant prefill `<think>\n\n</think>\n\n`
- Artifact roots:
  `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/` and
  `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/`

These are repo-native strict/pilot suites, not official BFCL, IFEval, or
HumanEval scores.

## Results

| Checkpoint | Suite | Cases | Passed | Pass rate | Residual failure |
|---|---|---:|---:|---:|---|
| Iter 100 | Held-out strict local tool-call | 8 | 8 | `1.000` | none |
| Iter 125 | Held-out strict local tool-call | 8 | 8 | `1.000` | none |
| Final 170 | Held-out strict local tool-call | 8 | 7 | `0.875` | `heldout-argument-correctness-lab-order` |
| Iter 100 | Mirrored regression | 6 | 5 | `0.833` | `argument-correctness-emr` |
| Iter 125 | Mirrored regression | 6 | 6 | `1.000` | none |
| Iter 100 | BFCL-style pilot | 3 | 2 | `0.667` | `bfcl-invalid-tool` |
| Iter 125 | BFCL-style pilot | 3 | 2 | `0.667` | `bfcl-invalid-tool` |
| Iter 100 | Coding sanity pilot | 3 | 2 | `0.667` | `coding-python-filter-even` |
| Iter 125 | Coding sanity pilot | 3 | 2 | `0.667` | `coding-python-filter-even` |
| Iter 100 | IFEval-style pilot | 3 | 3 | `1.000` | none |
| Iter 125 | IFEval-style pilot | 3 | 2 | `0.667` | `ifeval-forbidden-word` |

## Interpretation

Iteration 125 is the strongest strict Hermes candidate because it is the only
checked v6 checkpoint that passes both the held-out publication gate and the
mirrored regression suite at `1.000`.

Iteration 100 has a stronger IFEval pilot result, but it fails the mirrored
argument-correctness regression. Final iteration 170 is explicitly rejected
because it repeats the held-out lab-order failure. The training curve supports
this decision: validation loss reached its observed minimum near iteration 110
and then flattened/reversed.

The remaining pilot failures should be treated as a separate instruction-
following polish lane. They are not evidence against iter125 for strict Hermes
tool calls, but they do block claiming broad benchmark dominance.
