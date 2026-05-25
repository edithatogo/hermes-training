# Official Benchmark Environment

Date: 2026-05-25

## Decision

Official benchmark harnesses are installed in SSD-backed Python 3.12 virtual
environments, separate from the active Python 3.14 training environment.

Use two environments:

- General harness env: `/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312`
- BFCL env: `/Volumes/PortableSSD/hermes-training-envs/bfcl-py312`

BFCL is isolated because `bfcl-eval==2026.3.23` pins
`tree_sitter==0.21.3`, while `evalplus==0.3.1` requires
`tree-sitter>=0.22.0`.

## General Harness Env

Create or refresh:

```bash
python3.12 -m venv /Volumes/PortableSSD/hermes-training-envs/benchmarks-py312
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python -m pip install -U pip wheel setuptools
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python -m pip install \
  'lm_eval[hf,api]' evaluate human-eval evalplus mteb
```

Smoke check:

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python - <<'PY'
import importlib.metadata as md
import torch
for mod in ['lm_eval', 'langdetect', 'immutabledict', 'evaluate', 'evalplus', 'human_eval', 'mteb',
            'sentence_transformers', 'transformers']:
    __import__(mod)
for dist in ['lm_eval', 'langdetect', 'immutabledict', 'evaluate', 'evalplus', 'human-eval', 'mteb',
             'torch', 'transformers', 'sentence-transformers', 'tree-sitter']:
    print(dist, md.version(dist))
print('mps_available', torch.backends.mps.is_available())
PY
```

Verified versions:

| Package | Version |
|---|---|
| Python | 3.12.13 |
| `lm_eval` | 0.4.12 |
| `langdetect` | 1.0.9 |
| `immutabledict` | 4.3.1 |
| `evaluate` | 0.4.6 |
| `evalplus` | 0.3.1 |
| `human-eval` | 1.0.3 |
| `mteb` | 2.12.30 |
| `torch` | 2.12.0 |
| `transformers` | 5.9.0 |
| `sentence-transformers` | 5.5.1 |
| `tree-sitter` | 0.25.2 |
| Torch MPS | available |

`pip check` result: no broken requirements.

CLI smoke:

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval --help
```

Result: CLI starts and exposes `run`, `ls`, and `validate`.

## BFCL Env

Create or refresh:

```bash
python3.12 -m venv /Volumes/PortableSSD/hermes-training-envs/bfcl-py312
/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/python -m pip install -U pip wheel setuptools
/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/python -m pip install bfcl-eval soundfile
```

Smoke check:

```bash
/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/python - <<'PY'
import importlib.metadata as md
import tree_sitter
import bfcl_eval
import soundfile
for dist in ['bfcl-eval', 'soundfile', 'tree-sitter', 'numpy', 'torch',
             'transformers', 'sentence-transformers']:
    print(dist, md.version(dist))
PY
```

Verified versions:

| Package | Version |
|---|---|
| Python | 3.12.13 |
| `bfcl-eval` | 2026.3.23 |
| `soundfile` | 0.13.1 |
| `tree-sitter` | 0.21.3 |
| `numpy` | 1.26.4 |
| `torch` | 2.12.0 |
| `transformers` | 5.9.0 |
| `sentence-transformers` | 5.5.1 |

`pip check` result: no broken requirements.

CLI smoke:

```bash
/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl --help
```

Result: CLI starts and exposes `models`, `test-categories`, `generate`,
`evaluate`, `scores`, and `version`.

## Usage Rule

Use `benchmarks-py312` for `lm_eval`, MTEB, EvalPlus, HumanEval, and
embedding/retrieval benchmark harnesses.

Use `bfcl-py312` only for official BFCL runs.

Repo-native pilot suites remain runnable from the project `.venv` unless a
specific report says otherwise.
