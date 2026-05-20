# Repo Maintenance

This workspace is a hub repo with three submodule-style track repos:

- `gemma4`
- `lfm2`
- `ollama-pack`

The hub records the submodule commit pointers. Each track also has its own Git history and remote.

## Commit And Push Order

Use this order whenever a change spans a track repo and the hub root:

1. Commit/push `gemma4`.
2. Commit/push `lfm2`.
3. Commit/push `ollama-pack`.
4. Commit/push the hub root so its submodule pointers reference the pushed track commits.

Do not commit the hub first if submodules point at local-only commits. The hub should only record submodule SHAs that already exist on the remote for the nested repo.

## Submodule Pointer Rule

- Treat the hub root as a pointer manifest, not a place to store nested repo work.
- If a nested repo is dirty, leave its working tree alone and keep the hub root at the last known good pointer until that repo is committed and pushed.
- Never stage a hub-root submodule pointer update that refers to a commit which has not been pushed from the nested repo.
- When reviewing a hub-root diff, verify that each gitlink update matches a remote-visible nested repo commit.

## Nested Repo Dirty-State Checklist

Before changing the hub root, check the nested repos and record their state in `HANDOFF.md`:

- `gemma4`: dirty; tracked edits in `.gitignore`, `CONDUCTOR.md`, `README.md`, `scripts/build_dataset.py`, `scripts/run_train.sh`, `scripts/train.py`; untracked `conductor/`, `data/splits/valid.jsonl`, `scripts/train_config.gemma4-26b-a4b.experimental.yaml`, `scripts/train_config.hermes4-14b.experimental.yaml`, `scripts/train_config.qwen3-4b.smoke.yaml`, `scripts/train_config.qwen3.6-35b-a3b.experimental.yaml`
- `lfm2`: dirty; tracked edits in `.gitignore`, `CONDUCTOR.md`, `README.md`, `scripts/build_dataset.py`, `scripts/run_train.sh`, `scripts/train.py`; untracked `conductor/`, `data/splits/valid.jsonl`, `scripts/train_config.lfm25-1.2b-instruct.smoke.yaml`, `scripts/train_config.lfm25-1.2b-instruct.yaml`, `scripts/train_config.lfm25-1.2b-thinking.yaml`
- `ollama-pack`: dirty; tracked edits in `CONDUCTOR.md`, `README.md`; untracked `conductor/`, `modelfiles/LFM-Hermes.Modelfile`, `modelfiles/Qwen3-Hermes.Modelfile`, `scripts/create_experimental_safetensors.sh`, `scripts/runtime_smoke.sh`

## Generated Artifact Policy

Keep out of Git:

- LoRA adapters: `*.safetensors`
- local experiment directories: `experiments/`
- GGUF exports: `*.gguf`
- merged model directories
- Ollama export directories
- HTML eval reports unless intentionally published

Handle carefully:

- `data/raw/`
- `data/splits/`

Current smoke datasets are small and already live in the track repos. For future pilot/full datasets, prefer Hugging Face dataset repos or external storage rather than growing Git history.

## Current Cleanup Priorities

1. Verify submodule metadata:

   ```bash
   git submodule status --recursive
   ```

2. Verify model radar:

   ```bash
   python3 scripts/check_model_candidates.py
   ```

3. Verify syntax:

   ```bash
   bash -n gemma4/scripts/push_to_hf.sh lfm2/scripts/push_to_hf.sh
   python3 -m py_compile scripts/check_model_candidates.py
   ```

4. Decide whether to commit smoke data updates in `gemma4` and `lfm2`.

5. Train low-risk targets before large MoE experiments:

   - `LiquidAI/LFM2.5-1.2B-Instruct` (10-iteration smoke passed locally)
   - `Qwen/Qwen3-4B-MLX-4bit` (configured; retry after authenticated/prefetched HF download)
   - `LiquidAI/LFM2.5-1.2B-Thinking`

6. Treat these as runtime/baseline/teacher targets first:

   - `Qwen/Qwen3.6-35B-A3B`
   - `NousResearch/Hermes-4-14B`
   - `google/gemma-4-26B-A4B-it`
   - `Qwen/Qwen3-Next-80B-A3B-Instruct`

## Publication Rules

- GitHub: code, configs, cards, scripts, small smoke data if intentionally kept.
- Hugging Face datasets: pilot/full JSONL data.
- Hugging Face models: adapter-only releases by default.
- Ollama/LM Studio: GGUF artifacts only when redistribution license allows.
