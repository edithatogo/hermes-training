# Colab Packaging: Hermes Shortlist Offload Pack 20260612

Date: 2026-06-12
Status: `blocked`

## Purpose

Package the smallest reproducible Colab jobs for the Hermes shortlist track and
keep the artifact boundary bounded. This sheet is the execution handoff for the
current offload lane, not a benchmark claim.

## Packaged Jobs

| Job | Smallest script | Dispatcher form | Accelerator policy | Bounded artifacts |
|---|---|---|---|---|
| Accelerator smoke | `scripts/colab_smoke.py` | `colab run --gpu T4 --timeout 120 scripts/colab_smoke.py` | GPU-first; TPU only as a separate smoke if explicitly needed | stdout JSON, `reports/colab/<run-id>.md`, `/Volumes/PortableSSD/hermes-evals/colab/<run-id>/summary.json`, per-attempt `.log` files |
| Benchmark env smoke | `scripts/colab_benchmark_env_smoke.py` | `./.venv/bin/python scripts/colab_dispatch.py --accelerators gpu:T4,gpu:L4 --run-id <run-id> scripts/colab_benchmark_env_smoke.py --mode general --install-profile general-core` | GPU-first; TPU only after the script is XLA/JAX compatible | stdout JSON, `reports/colab/<run-id>.md`, `summary.json`, per-attempt `.log` files |
| Adaptive training smoke | `scripts/colab_adaptive_train_smoke.py 8 16` | `./.venv/bin/python scripts/colab_dispatch.py --allow-tpu --accelerators gpu:T4,tpu:v5e1 --retries 1 --timeout 240 --run-id <run-id> scripts/colab_adaptive_train_smoke.py 8 16` | GPU-first with TPU fallback only because the script is XLA-aware | stdout JSON, `reports/colab/<run-id>.md`, `summary.json`, per-attempt `.log` files |

## Hermes Shortlist Use

Use the same bounded package for the current shortlist lanes:

- `Qwen/Qwen3-4B-MLX-4bit`
- `Qwen/Qwen3.5-0.8B`
- `Qwen/Qwen3.5-2B`
- `openbmb/MiniCPM5-1B`
- Hermes 4.3 and Harmonic / Harmonic-Hermes comparison lanes
- Qwen3.6 teacher/runtime comparison lanes

The package does not download checkpoints into the repo and does not sync
anything beyond the bounded logs, summaries, and tracked reports.

## Artifact Boundary

- Keep checkpoints, caches, and datasets on the SSD-backed runtime root.
- Download only the log tails and JSON summaries needed to reproduce the run.
- Do not publish or commit remote artifacts that are larger than the tracked
  report, `summary.json`, or the per-attempt `.log` files.
- If a run requires checkpoint transfer back from Colab, mark the run blocked
  instead of widening the artifact surface.

## Current Blocker

`colab sessions` currently reports no active sessions. The package is ready for
dispatch, but execution remains blocked until a session is created.
