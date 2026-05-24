# Hermes Training Hub — Codex Handoff

> Last updated: 2026-05-24
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

Current working root is also available at
`/Volumes/PortableSSD/GitHub/hermes-training`.

## 2026-05-24 Storage Layout Update

The SSD root migration pass found that most top-level `/Volumes/PortableSSD`
folders are intentional artifact, cache, runtime, app-state, or media roots and
should not be moved into `GitHub`.

The only misplaced Git checkout was migrated:

- canonical checkout: `/Volumes/PortableSSD/GitHub/llama.cpp-convert-tool`
- legacy compatibility path:
  `/Volumes/PortableSSD/hermes-tools/llama.cpp ->
  /Volumes/PortableSSD/GitHub/llama.cpp-convert-tool`

Keep the legacy symlink in place because older scripts and notes refer to
`hermes-tools/llama.cpp`.

Validation added:

- `scripts/check_storage_layout.py`
- `tests/test_check_storage_layout.py`
- `scripts/validate_readiness.py` now runs the storage check when the SSD root
  is present.
- `scripts/repo_status.sh` now prints a `== storage layout ==` section.

The nested `ollama-pack` checkout has one related local edit:
`ollama-pack/scripts/export_ollama.sh` now resolves llama.cpp in this order:

1. `HERMES_LLAMA_CPP`
2. `$HERMES_STORAGE_ROOT/GitHub/llama.cpp-convert-tool`
3. `$HERMES_STORAGE_ROOT/hermes-tools/llama.cpp`

Commit order if preserving this work:

1. Commit/push the nested `ollama-pack` change first.
2. Commit/push the hub root after the nested commit is available remotely.

Validation commands that passed:

```bash
scripts/repo_status.sh
./scripts/check_storage_layout.py --root /Volumes/PortableSSD
PYTHONPATH=. python3 -m unittest discover -s tests
./.venv/bin/python scripts/validate_readiness.py
```

The audit report is
`reports/storage/root-migration-audit-20260524.md`.

## Repo Hygiene Status

The hub and nested repos were cleaned, committed, and pushed before the latest runtime/documentation pass. Treat the current working tree as the source of truth and check status before committing:

```bash
git status --short
git -C gemma4 status --short
git -C lfm2 status --short
git -C ollama-pack status --short
```

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
- Azure preflight exists at `scripts/azure_preflight.py`; it now passes for `d.a.mordaunt@gmail.com` on `Azure for Students`. Modern GPU quota is zero across sampled regions, so the Azure track is fail-closed until quota is approved.

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
- Qwen3 4B dequantized fused export and GGUF conversion are complete on the SSD:
  - `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/merged-dequantized`
  - `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-f16.gguf`
  - `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`
- The Q4_K_M GGUF passed direct `llama-completion` validation and returned `{"ok": true}`. Ollama GGUF import failed because the daemon dropped during model creation, so LM Studio/direct llama.cpp is the next GGUF runtime path.
- Populated publication drafts for the Qwen3 smoke run exist in `reports/publication/qwen3-4b-smoke/`.
- Internal disk pressure has been reduced. `~/.gemini/antigravity/browser_recordings` was relocated to `/Volumes/PortableSSD/home-relocated/gemini-antigravity/browser_recordings` and symlinked back. Last check showed about 51 GiB free on `/` and about 660 GiB free on `/Volumes/PortableSSD`.

## Next Actions

1. Validate the Qwen3 Q4_K_M GGUF in LM Studio and record the OpenAI-compatible smoke result.
2. Re-test Ollama only after upgrading or replacing the current crashing Qwen3 GGUF/import path.
3. Confirm Azure ML GPU quota/capacity before creating any workspace compute or submitting benchmark jobs.
4. Use the non-spending Azure job templates for a benchmark-only smoke job only after quota/capacity is confirmed.
5. Start a safer LFM2.5 recipe only with lower learning rate and an early empty-response gate.
6. Use Qwen3 4B as the next local MLX candidate; use Hermes 4 and Qwen3.6 as runtime baselines/teachers before local fine-tunes.
7. Validate every runtime through `ollama-pack/scripts/runtime_smoke.sh` before using it in Hermes.
8. Do not publish the Qwen3 smoke adapter as a quality artifact; the publication drafts exist to show provenance shape only.

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
