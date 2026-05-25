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

## Nested Repo State Checklist

Before changing the hub root, check the nested repos and record their state in
`HANDOFF.md`.

Current pushed pointers as of 2026-05-25:

- `gemma4`: `d4d7078`, clean after Qwen3 v5 non-promotion documentation.
- `lfm2`: `40c4020`, clean.
- `ollama-pack`: `c740e96`, clean after runtime packaging track closure.

If any nested repo becomes dirty, commit and push that repo before staging the
hub submodule pointer.

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
   scripts/repo_status.sh
   ```

2. Verify storage layout directly when working on SSD organization:

   ```bash
   ./scripts/check_storage_layout.py --root /Volumes/PortableSSD
   ```

3. Verify model radar:

   ```bash
   python3 scripts/check_model_candidates.py
   ```

4. Verify syntax:

   ```bash
   bash -n gemma4/scripts/push_to_hf.sh lfm2/scripts/push_to_hf.sh
   python3 -m py_compile scripts/check_model_candidates.py
   ```

5. Keep v4 as the recommended/public Qwen3 adapter; do not promote v5.

6. Train low-risk targets before large MoE experiments:

   - `LiquidAI/LFM2.5-1.2B-Instruct` (10-iteration smoke passed locally)
   - `Qwen/Qwen3-4B-MLX-4bit` (local strict-tool-call v4 adapter is the current recommended adapter)
   - `LiquidAI/LFM2.5-1.2B-Thinking`

7. Treat these as runtime/baseline/teacher targets first:

   - `Qwen/Qwen3.6-35B-A3B`
   - `NousResearch/Hermes-4-14B`
   - `google/gemma-4-26B-A4B-it`
   - `Qwen/Qwen3-Next-80B-A3B-Instruct`

## Publication Rules

- GitHub: code, configs, cards, scripts, small smoke data if intentionally kept.
- Hugging Face datasets: pilot/full JSONL data.
- Hugging Face models: adapter-only releases by default.
- Ollama/LM Studio: GGUF artifacts only when redistribution license allows.
