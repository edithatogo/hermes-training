# Cloud Dynamic Benchmark Orchestration

This is the operator workflow for routing Hermes, mem0, frontier, and runtime
benchmark jobs across local execution, Colab, Hugging Face Jobs, Azure,
NVIDIA NGC, and Kaggle lanes.

The registry is `CLOUD_BENCHMARK_ORCHESTRATION.yaml`.

## Backend Order

1. Local Mac/Metal remains the proof lane for MLX, Ollama, LM Studio, llama.cpp,
   and current-system compatibility.
2. Colab is the first remote execution lane for sanitized, bounded GPU or
   TPU-compatible jobs.
3. Hugging Face Jobs is the first persistent remote lane for public PEFT
   scorecards after prepaid credits or grant capacity are available.
4. Azure is prepared only after login, subscription, Azure ML extension, quota,
   region, and cost checks pass.
5. NVIDIA NGC is prepared only after API key or SSO, org/team, entitlement,
   Cloud Function GPU quota, registry/container,
   model, and license checks pass.
6. Kaggle is prepared only after CLI authentication and quota checks pass.

## Read-Only Backend Registry

Run:

```bash
source scripts/env.sh
PATH="$HOME/.local/bin:$PATH" ./.venv/bin/python scripts/cloud_backend_preflight.py
```

This writes:

- `reports/cloud/backend-preflight-20260613.json`
- `reports/cloud/backend-preflight-20260613.md`

The preflight does not create sessions, log in, submit jobs, upload data, or
spend money. A blocked provider is recorded as blocked instead of making the
whole registry fail.

To generate the current operator unblock checklist:

```bash
./.venv/bin/python scripts/build_cloud_unblock_checklist.py
```

This writes:

- `reports/cloud/backend-unblock-checklist-20260613.json`
- `reports/cloud/backend-unblock-checklist-20260613.md`

## Colab Dispatch

Use Colab for bounded, sanitized jobs:

```bash
source scripts/env.sh
PATH="$HOME/.local/bin:$PATH" ./.venv/bin/python scripts/colab_dispatch.py \
  --accelerators gpu:T4,gpu:L4 \
  --retries 1 \
  --timeout 300 \
  --run-id <run-id> \
  scripts/colab_smoke.py
```

For the benchmark environment smoke:

```bash
PATH="$HOME/.local/bin:$PATH" ./.venv/bin/python scripts/colab_dispatch.py \
  --accelerators gpu:T4 \
  --retries 1 \
  --timeout 1200 \
  --run-id <run-id> \
  scripts/colab_benchmark_env_smoke.py \
    --mode general \
    --install-profile general-core \
    --install-timeout 900
```

TPU stays opt-in:

```bash
PATH="$HOME/.local/bin:$PATH" ./.venv/bin/python scripts/colab_dispatch.py \
  --allow-tpu \
  --accelerators gpu:T4,tpu:v5e1 \
  --timeout 240 \
  --run-id <run-id> \
  scripts/colab_adaptive_train_smoke.py 8 16
```

## Job Profiles

| Profile | Primary route | Output |
|---|---|---|
| `hermes-runtime-smoke` | local, then Colab | runtime summary and run card |
| `standard-benchmark-slice` | Colab, then HF Jobs, then Azure/Kaggle | environment versions, manifest, scorecard or blocker |
| `mem0-embedding-reranker-sweep` | local, then Colab | retrieval metrics and migration gate |
| `runtime-packaging-proof` | local, Colab, then NGC | runtime command, return code, log tail |
| `frontier-support-evaluation` | Colab, HF Jobs/Azure/Kaggle, then NGC | provider, license, benchmark slice, publication boundary |

## Stop Conditions

Stop before execution when any of these are true:

- credentials are missing
- compute would be paid and explicit approval is absent
- license or terms are restricted or unknown
- the job needs private memory data, secrets, or unapproved datasets
- the artifact boundary is unbounded
- provider quota, entitlement, or capacity is missing

## Artifact Boundary

Tracked files should be compact run cards, manifests, summaries, and reports.
Remote logs and `summary.json` belong under `/Volumes/PortableSSD/hermes-evals`.
Model caches, datasets, checkpoints, raw benchmark outputs, and remote workdirs
must stay out of git unless a later publication gate explicitly approves them.

## Current Backend State

As of the 2026-06-13 registry:

- Colab CLI `0.5.11` is ready and `colab sessions` reports no active session.
  Bounded PEFT pilots work; no-limit full scorecard runs remain blocked by
  session pruning/keepalive permission failures.
- Hugging Face Jobs is authenticated as `edithatogo`, exposes GPU hardware, and
  has a guarded scorecard submitter, but live jobs are blocked by insufficient
  prepaid credits.
- Azure CLI is installed, but `az account show` currently requires `az login`;
  quota/cost checks must be rerun after login.
- NGC is installed but unconfigured; the viable route appears to be Cloud
  Function tasks after SSO/API key, org/team, GPU quota, registry access,
  benchmark container, and result persistence are proven.
- Kaggle CLI `2.2.1` is installed, and a guarded kernel scorecard lane is
  staged, but authentication and quota checks are still required.
