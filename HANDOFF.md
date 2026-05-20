# Hermes Training Hub — Codex Handoff

> Last updated: 2026-05-21
> Pickup agent: Codex

## What Is Here

All under `/Users/doughnut/GitHub/hermes-training/`:

| Repo | GitHub | Purpose |
|---|---|---|
| `gemma4/` | `github.com/edithatogo/hermes-gemma-lab` | Gemma/Qwen/Hermes 4 smoke configs and local fine-tune scripts |
| `lfm2/` | `github.com/edithatogo/hermes-lfm2-lab` | LFM/LFM2.5/LFM2/Ministral configs and local fine-tune scripts |
| `ollama-pack/` | `github.com/edithatogo/hermes-ollama-pack` | Ollama, experimental safetensors, GGUF, and Hermes runtime scripts |
| hub root | `github.com/edithatogo/hermes-training` | Platform lanes, model radar, requirements, runtime strategy, Azure scale-out, submodule map |

The hub root tracks the model repos as Git submodules. `.gitmodules` has been added to repair the previous gitlink-without-submodule metadata state.

## Repo Hygiene Status

Current working trees are dirty in the hub root and nested track repos. The current verified state is:

- Hub root: dirty, with maintenance docs and repo-structure files added or edited.
- `gemma4/`: dirty; tracked edits in `.gitignore`, `CONDUCTOR.md`, `README.md`, `scripts/build_dataset.py`, `scripts/run_train.sh`, `scripts/train.py`; untracked `conductor/`, `data/splits/valid.jsonl`, `scripts/train_config.gemma4-26b-a4b.experimental.yaml`, `scripts/train_config.hermes4-14b.experimental.yaml`, `scripts/train_config.qwen3-4b.smoke.yaml`, `scripts/train_config.qwen3.6-35b-a3b.experimental.yaml`.
- `lfm2/`: dirty; tracked edits in `.gitignore`, `CONDUCTOR.md`, `README.md`, `scripts/build_dataset.py`, `scripts/run_train.sh`, `scripts/train.py`; untracked `conductor/`, `data/splits/valid.jsonl`, `scripts/train_config.lfm25-1.2b-instruct.smoke.yaml`, `scripts/train_config.lfm25-1.2b-instruct.yaml`, `scripts/train_config.lfm25-1.2b-thinking.yaml`.
- `ollama-pack/`: dirty; tracked edits in `CONDUCTOR.md`, `README.md`; untracked `conductor/`, `modelfiles/LFM-Hermes.Modelfile`, `modelfiles/Qwen3-Hermes.Modelfile`, `scripts/create_experimental_safetensors.sh`, `scripts/runtime_smoke.sh`.

Do not modify nested repos just to clean the hub. Treat these as separate commit/push units and record pointer changes only after the nested commit exists on the remote.

## Current State

Complete:

- Proper Conductor structures now exist at the hub and nested track levels:
  - `conductor/`
  - `lfm2/conductor/`
  - `gemma4/conductor/`
  - `ollama-pack/conductor/`
- Repo scaffolding for current tracks.
- Real Hermes smoke dataset exists in the model tracks.
- Dataset pipeline writes train/val/test JSONL.
- MLX LoRA training script exists.
- Eval/comparison scripts exist.
- Hugging Face publishing scripts use the current `hf` CLI.
- Runtime docs cover Ollama launcher, experimental safetensors, GGUF, MLX, LM Studio, and KTransformers.
- Model radar includes Qwen3.6, Hermes 4, Gemma 4 A4B, LFM2.5, LFM2-ColBERT, Qwen3-Next, BitNet, BGE-M3, Jina embeddings, and watchlist entries for RWKV/Mamba-style families.
- Platform abstraction is now explicit: Mac/MLX is the local lane, Azure is the scale-out lane, retrieval is separate from chat SFT, and specialist runtimes require proof.
- Azure preflight exists at `scripts/azure_preflight.py`; it now passes for `d.a.mordaunt@gmail.com` on `Azure for Students`.

Current gaps:

- LFM2.5 smoke adapter exists locally under `lfm2/experiments/lfm25-1.2b-instruct-smoke/lora_adapter`; it is intentionally ignored by Git.
- Hugging Face repos are planned, not published.
- Large MoE configs are smoke configs only; do not treat them as safe defaults for local training.
- Nested repos still have dirty changes and need an intentional commit/push pass.
- Current checked-in dataset scale is smoke only, not publishable fine-tuning data.
- Qwen3 4B MLX smoke config exists, but unauthenticated model download stalled during first proof attempt.
- Azure student subscription login is complete. GPU-family quota/capacity still needs explicit Azure ML/portal confirmation before compute creation.
- LFM2.5 full-smoke training/evaluation is complete as a proof, but the adapter is not publishable. It trained for 200 iterations / 175,895 tokens with final validation loss 1.455 and peak memory 6.022 GB; evaluation on 100 prompts showed response collapse. See `lfm2/eval/lfm25-full-smoke-summary.md`.
- Qwen3 4B smoke training/evaluation is complete as a local MLX proof. It trained for 10 iterations / 2,889 tokens with final validation loss 2.386 and peak memory 3.944 GB; base and adapter both passed the response-collapse gate. See `gemma4/eval/qwen3-4b-smoke-summary.md`.
- Qwen3 4B MLX adapter runtime smoke passed through an OpenAI-compatible `mlx_lm.server` endpoint. See `ollama-pack/runtime-card.qwen3-4b-mlx-smoke.md`.
- Qwen3 4B fused safetensors export exists under `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke`. Ollama experimental import succeeded into `/Volumes/PortableSSD/ollama-models`, but `/v1/chat/completions` failed with an Ollama MLX runner panic, so Ollama is not a validated runtime for this Qwen3 package yet.
- Internal disk pressure has been reduced. `~/.gemini/antigravity/browser_recordings` was relocated to `/Volumes/PortableSSD/home-relocated/gemini-antigravity/browser_recordings` and symlinked back. Last check showed about 51 GiB free on `/` and about 660 GiB free on `/Volumes/PortableSSD`.

## Next Actions

1. Commit/push the nested track repos in this order: `gemma4`, `lfm2`, then `ollama-pack`.
2. Update the hub root only after the nested repo commits are pushed, so the submodule pointers reference remote-visible SHAs.
3. Retry Qwen3 4B with a valid `HF_TOKEN` or prefetch the model into `/Volumes/PortableSSD/huggingface`.
4. Confirm Azure ML GPU quota/capacity for the target region before creating compute.
5. Use the non-spending Azure job templates for a benchmark-only smoke job only after quota/capacity is confirmed.
6. Start a safer LFM2.5 recipe only with lower learning rate and an early empty-response gate.
7. Decide whether to keep smoke datasets and eval JSONL outputs in Git or move generated data out of future commits.
8. Use Qwen3 4B as the next local MLX candidate; use Hermes 4 and Qwen3.6 as runtime baselines/teachers before local fine-tunes.
9. Validate every runtime through `ollama-pack/scripts/runtime_smoke.sh` before using it in Hermes.
10. Treat Ollama/LM Studio as pending until a stable Qwen3 GGUF converter or Ollama safetensors runtime path is proven. MLX server is the current validated local runtime.

## Key Files

| File | What to edit |
|---|---|
| `conductor/tracks.md` | Hub-level track registry |
| `conductor/tracks/*/spec.md` | Hub-level feature specifications |
| `conductor/tracks/*/plan.md` | Hub-level implementation plans |
| `MODEL_CANDIDATES.yaml` | Machine-readable model radar |
| `PLATFORM_LANES.md` | Purpose/platform abstraction and lane routing |
| `AZURE_SCALEOUT.md` | Azure preflight and cloud-lane policy |
| `scripts/check_model_candidates.py` | HF existence/status verification |
| `FRAMEWORKS.md` | Framework and SDK choices |
| `RUNTIME_TARGETS.md` | Runtime/serving strategy |
| `scripts/train_config*.yaml` | Model ID, batch size, iterations |
| `modelfiles/*.Modelfile` | Chat template/runtime packaging |

## Read First

- `README.md`
- `BENCHMARKING_PLAN.md`
- `STANDARD_BENCHMARKS.md`
- `DOCUMENTATION_PLAN.md`
- `APPLICATIONS.md`
- `REQUIREMENTS.md`
- `FUTURE_MODELS.md`
- `FRAMEWORKS.md`
- `RUNTIME_TARGETS.md`
- `NEW_MODEL_WORKFLOW.md`
