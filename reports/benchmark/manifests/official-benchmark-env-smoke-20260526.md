# Official Benchmark Environment Smoke

Date: 2026-05-26

## Decision

The SSD-backed official benchmark environments are runnable. This is
environment readiness evidence only; it is not an official BFCL, IFEval,
lm-eval, HumanEval, EvalPlus, or MTEB score for any model or adapter.

Generated smoke outputs are stored outside the git repo on the SSD:

```text
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/env-smoke/general-20260526.json
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/env-smoke/bfcl-20260526.json
```

## General Harness Environment

Command:

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python \
  scripts/smoke_official_benchmark_env.py \
  --mode general \
  --json-output /Volumes/PortableSSD/hermes-evals/standard-benchmarks/env-smoke/general-20260526-after-ifeval-deps.json
```

Result: passed.

| Check | Result |
|---|---|
| Python | `3.12.13` |
| Executable | `/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python` |
| Imports | `lm_eval`, `langdetect`, `immutabledict`, `evaluate`, `evalplus`, `human_eval`, `mteb`, `sentence_transformers`, `transformers`, `torch` |
| `pip check` | no broken requirements |
| `lm_eval --help` | starts successfully |
| Torch MPS | available |

Versions:

| Package | Version |
|---|---|
| `lm_eval` | `0.4.12` |
| `langdetect` | `1.0.9` |
| `immutabledict` | `4.3.1` |
| `evaluate` | `0.4.6` |
| `evalplus` | `0.3.1` |
| `human-eval` | `1.0.3` |
| `mteb` | `2.12.30` |
| `torch` | `2.12.0` |
| `transformers` | `5.9.0` |
| `sentence-transformers` | `5.5.1` |
| `tree-sitter` | `0.25.2` |

## BFCL Environment

Command:

```bash
/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/python \
  scripts/smoke_official_benchmark_env.py \
  --mode bfcl \
  --json-output /Volumes/PortableSSD/hermes-evals/standard-benchmarks/env-smoke/bfcl-20260526-after-soundfile.json
```

Result: passed.

| Check | Result |
|---|---|
| Python | `3.12.13` |
| Executable | `/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/python` |
| Imports | `bfcl_eval`, `soundfile`, `tree_sitter`, `numpy`, `torch`, `transformers`, `sentence_transformers` |
| `pip check` | no broken requirements |
| `bfcl --help` | starts successfully |
| Torch MPS | available |

Versions:

| Package | Version |
|---|---|
| `bfcl-eval` | `2026.3.23` |
| `soundfile` | `0.13.1` |
| `tree-sitter` | `0.21.3` |
| `numpy` | `1.26.4` |
| `torch` | `2.12.0` |
| `transformers` | `5.9.0` |
| `sentence-transformers` | `5.5.1` |

## Boundary

Use this report to prove the benchmark harnesses are installed, isolated, and
runnable on SSD-backed environments. Do not use it as model quality evidence.

Official benchmark score tracks still need separate run cards that record the
model, adapter, prompt profile, dataset/task names, versions, seeds, raw output
paths, and pass/fail interpretation.
