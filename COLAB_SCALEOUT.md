# Colab CLI Scale-Out

Google's `google-colab-cli` is a useful burst-compute lane for this project.
It does not replace Mac/MLX runtime proof or Azure as the formal scale-out lane,
but it can close a practical gap while Azure GPU quota is unavailable.

## When To Use It

Use Colab CLI for:

- bounded official benchmark scorecards that need CUDA but not a durable cluster
- teacher/evaluator runs for Gemma, Qwen, Hermes, LFM, MiniCPM, BitNet, or
  Nemotron candidates when artifacts can be synced back immediately
- runtime smoke tests for CUDA/NVIDIA-only packages before deciding whether an
  Azure job is worth requesting
- short LoRA or QLoRA experiments where checkpoint loss is acceptable and every
  artifact is downloaded at the end of the run

Do not use Colab CLI for:

- Mac/MLX runtime claims
- Ollama, LM Studio, or llama.cpp-on-Mac validation
- long-running training where preemption would waste too much work
- private dataset publication without a separate privacy and credential review
- claims that require a reproducible managed cluster or fixed cloud image

## Install

Prefer an isolated user-level install:

```bash
uv tool install google-colab-cli
```

Fallback:

```bash
pipx install google-colab-cli
```

The older PyPI package named `colab-cli` is a notebook/Drive workflow helper and
is not the same tool. Use Google's `google-colab-cli` package, which exposes the
`colab` command.

## Read-Only Preflight

Run from the hub:

```bash
source scripts/env.sh
./.venv/bin/python scripts/colab_preflight.py
```

The preflight checks whether `colab` is installed, records the local version
command result, verifies that the SSD storage root is available, and prints the
first safe smoke commands. It does not create a Colab session, spend compute, or
upload files.

## First Smoke

After confirming the account and any Colab plan/compute-unit constraints, run a
single disposable GPU smoke:

```bash
colab run --gpu T4 scripts/colab_smoke.py --output-dir /content/hermes-colab-smoke
```

Then download or emit the report back to:

```text
/Volumes/PortableSSD/hermes-evals/colab/
```

## Candidate Job Order

1. Official benchmark environment smoke on a T4 or L4 runtime.
2. Direct `lm_eval` selected-task candidate run for the current Qwen3 v4 adapter.
3. Gemma 4 QAT GGUF runtime smoke if the runtime supports the package shape.
4. MiniCPM5-1B fast utility prompt smoke.
5. NVIDIA Nemotron runtime smoke only on an NVIDIA-capable Colab runtime.

## Run Card Requirements

Every Colab run must record:

- Colab CLI version and command
- runtime accelerator requested and actual accelerator observed
- model IDs, quantization, and licenses
- input dataset or benchmark manifest
- output directory and files downloaded to the SSD
- wall-clock runtime and failure mode
- whether the result is a smoke, candidate-pilot, or full benchmark claim

Use [templates/colab/run-card.md](./templates/colab/run-card.md) for the run
card shape.
