# Colab CLI Scale-Out

Google's `google-colab-cli` is a useful burst-compute lane for this project.
It does not replace Mac/MLX runtime proof or Azure as the formal scale-out lane,
but it can close a practical gap while Azure GPU quota is unavailable.

## When To Use It

Verified local status on 2026-06-11:

- `colab` is installed at `/Users/doughnut/.local/bin/colab`
- version `0.5.9`
- T4 CUDA smoke passed
- TPU `v5e1` smoke passed through `torch_xla` / `xla:0`

Adaptive training status on 2026-06-12:

- availability-aware training dispatch selected `gpu:T4` and completed a tiny
  PyTorch training run on CUDA
- retry-enabled `gpu:T4` training completed successfully
- forced `tpu:v5e1` training was blocked by transient Colab assignment/socket
  errors before the script could run
- forced `tpu:v6e1` training was rejected by Colab for quota or entitlement

Policy: use GPU-first dispatch for real training. Include TPU only when the
script is explicitly JAX/PyTorch-XLA compatible and the run can tolerate Colab
TPU availability failures.

Use Colab CLI for:

- bounded official benchmark scorecards that need CUDA but not a durable cluster
- teacher/evaluator runs for Gemma, Qwen, Hermes, LFM, MiniCPM, BitNet, or
  Nemotron candidates when artifacts can be synced back immediately
- runtime smoke tests for CUDA/NVIDIA-only packages before deciding whether an
  Azure job is worth requesting
- TPU-compatible JAX or PyTorch/XLA experiments, especially small architecture
  probes that do not depend on CUDA-specific kernels
- short LoRA or QLoRA experiments where checkpoint loss is acceptable and every
  artifact is downloaded at the end of the run

Do not use Colab CLI for:

- Mac/MLX runtime claims
- Ollama, LM Studio, or llama.cpp-on-Mac validation
- long-running training where preemption would waste too much work
- private dataset publication without a separate privacy and credential review
- claims that require a reproducible managed cluster or fixed cloud image
- CUDA-only scripts on TPU runtimes

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
colab run --gpu T4 --timeout 120 scripts/colab_smoke.py
```

For TPU:

```bash
colab run --tpu v5e1 --timeout 180 scripts/colab_smoke.py
```

Capture the local output and emit the report back to:

```text
/Volumes/PortableSSD/hermes-evals/colab/
```

## Availability-Aware Dispatch

Use `scripts/colab_dispatch.py` when a job can run on more than one accelerator
and should choose based on availability:

```bash
./.venv/bin/python scripts/colab_dispatch.py \
  --accelerators gpu:T4,gpu:L4,gpu:A100 \
  --retries 1 \
  --run-id colab-auto-gpu-smoke-20260611 \
  scripts/colab_smoke.py
```

For jobs that really support TPU/XLA or JAX:

```bash
./.venv/bin/python scripts/colab_dispatch.py \
  --allow-tpu \
  --accelerators gpu:T4,gpu:L4,tpu:v5e1,tpu:v6e1 \
  --retries 1 \
  --run-id colab-auto-gpu-tpu-smoke-20260611 \
  scripts/colab_smoke.py
```

The dispatcher tries accelerators in order and stops after the first successful
run. It writes:

- per-attempt logs under `/Volumes/PortableSSD/hermes-evals/colab/<run-id>/`
- `summary.json` under the same SSD directory
- a tracked report under `reports/colab/<run-id>.md`

TPU remains opt-in because most current training and benchmark scripts use CUDA,
Metal, llama.cpp, or Transformers GPU paths that do not automatically translate
to PyTorch/XLA.

The adaptive training smoke proves this policy with a tiny synthetic PyTorch
training job:

```bash
./.venv/bin/python scripts/colab_dispatch.py \
  --allow-tpu \
  --accelerators gpu:T4,tpu:v5e1 \
  --retries 1 \
  --timeout 240 \
  --run-id colab-adaptive-train-auto-20260612 \
  scripts/colab_adaptive_train_smoke.py 8 16
```

To force TPU/XLA training proof:

```bash
./.venv/bin/python scripts/colab_dispatch.py \
  --allow-tpu \
  --accelerators tpu:v5e1 \
  --retries 1 \
  --timeout 300 \
  --run-id colab-adaptive-train-tpu-v5e1-20260612 \
  scripts/colab_adaptive_train_smoke.py 8 16
```

Current TPU caveat: `v5e1` allocation can be transiently unavailable, and
`v6e1` may require quota or entitlement not present on this account. Keep a GPU
fallback in the accelerator list unless the job is TPU-only by design.

## Candidate Job Order

1. Official benchmark environment smoke on a T4 or L4 runtime through
   `scripts/colab_dispatch.py`.
2. Direct `lm_eval` selected-task candidate run for the current Qwen3 v4 adapter.
3. Gemma 4 QAT GGUF runtime smoke if the runtime supports the package shape.
4. MiniCPM5-1B fast utility prompt smoke.
5. NVIDIA Nemotron runtime smoke only on an NVIDIA-capable Colab runtime.
6. TPU-only experiments only after the script has a JAX or PyTorch/XLA path.

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

For training jobs, fill out
[templates/colab/training-job-plan.md](./templates/colab/training-job-plan.md)
first. TPU should only be included in `scripts/colab_dispatch.py --allow-tpu`
when that plan marks the script as XLA/JAX compatible.
