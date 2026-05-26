# Adding a New Model — Conductor Workflow

## 1-Minute Checklist

Changing from one base model to another usually requires touching **3-5 files:**

```bash
# 1. Create new repo from template
cp -r /Volumes/PortableSSD/GitHub/hermes-training/gemma4 /Volumes/PortableSSD/GitHub/hermes-training/{new-model}

# 2. Change the MODEL ID in the training config or create a sibling config
sed -i '' 's|google/gemma-4-E4B-it|huggingface/{model-id}|' {new-model}/scripts/train_config.yaml

# 3. Write a model-specific Modelfile/runtime entry
#    (different chat template format per model)
vim {new-model}/modelfiles/{ModelName}.Modelfile
```

## What's Already Automated

The pipeline handles everything else automatically:

| What | How | File |
|------|-----|------|
| Dataset loading | Reads `data/splits/` (same format for any model) | `build_dataset.py` |
| MLX LoRA training | Parameterized via config YAML | `train.py` |
| Model download | Auto-downloads via `mlx_lm.load()` to SSD | `train.py` |
| Evaluation | Works with any loaded model | `evaluate.py` |
| Side-by-side comparison | Compares any two models | `compare.py` |
| GGUF conversion | llama.cpp/Ollama converter when architecture is supported | `export_ollama.sh` |
| Ollama packaging | GGUF path or experimental safetensors path | `export_ollama.sh`, `ollama-pack/scripts/create_experimental_safetensors.sh` |
| Hermes launch | Ollama configures Hermes provider/model | `ollama launch hermes` |

## Qwen3 Smoke Prep Path

For Qwen3 smoke work in this repo, use the hub-level SSD-backed cache script first:

```bash
source /Volumes/PortableSSD/GitHub/hermes-training/scripts/env.sh
export HF_TOKEN=...
```

Then prefetch with the cache rooted on the SSD volume:

```bash
HF_HOME="$HERMES_STORAGE_ROOT/huggingface" \
HF_HUB_CACHE="$HERMES_STORAGE_ROOT/huggingface/hub" \
hf download Qwen/Qwen3-4B-MLX-4bit
```

Verification and dry-run before any actual training:

```bash
test "$HF_HOME" = "/Volumes/PortableSSD/huggingface"
cd /Volumes/PortableSSD/GitHub/hermes-training/gemma4
../.venv/bin/python scripts/train.py --config scripts/train_config.qwen3-4b.smoke.yaml --dry-run
```

Blockers to record before starting the smoke run:

- missing `HF_TOKEN`
- inaccessible or unwritable SSD cache path
- stale partial model cache from an interrupted prefetch
- system `python3` lacks `mlx_lm`; use the repo venv instead
- dry run output that does not match the Qwen3 smoke config

## Creating a New Model Track

```bash
# Run this from the hub:
cd /Volumes/PortableSSD/GitHub/hermes-training

# 1. Clone the template
cp -r gemma4 new-model-name

# 2. Remove old git history
rm -rf new-model-name/.git
rm -rf new-model-name/data/raw/hermes3_dataset.jsonl
rm -rf new-model-name/experiments

# 3. Update config — only model ID changes
#    train_config.yaml → change 'model' field

# 4. Create Modelfile for the new model's chat template
#    (gemma4 uses <|start_header_id|>, LFM2 uses <|im_start|>)

# 5. Init git and push
cd new-model-name
git init -b main
git add -A
git commit -m "feat: scaffold {model-name} Hermes fine-tune"
gh repo create hermes-{model-name}-lab --private --source . --remote origin --push

# 6. Download dataset + model
HF_HOME=/Volumes/PortableSSD/huggingface python3 scripts/download_hermes_dataset.py

# 7. Train
HF_HOME=/Volumes/PortableSSD/huggingface python3 scripts/train.py --config scripts/train_config.yaml

# 8. Export or create runtime package
bash scripts/export_ollama.sh experiments/{adapter-dir} {model-name}-hermes

# Alternative: local Ollama experimental safetensors path, when supported
bash ../ollama-pack/scripts/create_experimental_safetensors.sh /path/to/hf-model-dir {model-name}-hermes ../ollama-pack/modelfiles/{ModelName}.Modelfile

# 9. Validate the Hermes-facing endpoint
bash ../ollama-pack/scripts/runtime_smoke.sh {model-name}-hermes
ollama launch hermes
```

## What Must Change Per Model

Only these parts are model-specific:

| Component | Why It Differs | Example |
|-----------|---------------|---------|
| `train_config.yaml:model` | Different HuggingFace ID | `google/gemma-4-E4B-it` → `google/recurrentgemma-2b-it` |
| `Modelfile TEMPLATE` | Different chat template format | Qwen/LFM: ChatML-like, Gemma/RecurrentGemma: Gemma turn tags, Mistral/Ministral: `[INST]` |
| `Modelfile FROM` | Different base model, safetensors dir, or GGUF path | `FROM __MODEL_DIR__`, `FROM ./model.gguf` |
| `train_config.yaml:batch_size` | Memory varies by model size | 4B model: batch 4 → 9B model: batch 2 |
| `CONDUCTOR.md` | Track updates | Model name, license, status |

## Radar Promotion Checklist

Before adding a model to a runnable training or benchmark track, update `MODEL_CANDIDATES.yaml` with:

- `role`: local-finetune, local-runtime, cloud-teacher, cloud-finetune, retrieval, research-runtime, or watchlist
- `environment`: mac-mlx, mac-ollama, mac-lmstudio, azure-cuda, hf-transformers, retrieval, or specialist-runtime
- `feasibility`: ready, needs-auth, needs-runtime-proof, cloud-only, or speculative
- `first_runtime`: the first validated runtime path, not a guess
- `first_finetune`: the first validated training path, or `defer` if the model is runtime-only
- `notes`: the current promotion limit, including `needs-runtime-proof` or `watchlist` where applicable

Use the matching gate for the role before promoting the model:

| Role | Required gate | Publication limit |
|---|---|---|
| `local-finetune` | Dataset audit, runtime proof, Hermes-local benchmark, and lane-specific benchmark gate | Adapter-only unless redistribution is explicitly allowed. |
| `local-runtime` | Runtime proof and Hermes prompt smoke | Runtime notes only. |
| `cloud-teacher` | Teacher-eval gate plus Hermes prompt smoke | Model card and comparison notes only. |
| `cloud-finetune` | Full benchmark gate | Adapter publication only if the license allows it. |
| `retrieval` | Retrieval benchmark gate | Retrieval artifacts and notes only. |
| `research-runtime` | Runtime proof only | No benchmark claim until promoted. |
| `watchlist` | None until promoted | Docs/spec notes only. |

Keep a model as `watchlist`/`speculative` until all of these are known:

- model card or primary release note
- available weights or quantization
- license and redistribution limits
- first runtime path
- benchmark gate that matches the model role

## What Stays Identical Across Models

| Component | Why It's the Same |
|-----------|------------------|
| `build_dataset.py` | Data format is model-agnostic (JSONL messages) |
| `train.py` | mlx-lm handles all HuggingFace transformers |
| `evaluate.py` | Works with any model loaded via mlx_lm |
| `compare.py` | Compares any two models |
| `download_hermes_dataset.py` | Sources same Hermes data, format is universal |
| `export_ollama.sh` | Generic script, only needs adapter path + model name |
| `push_to_hf.sh` | Generic, only needs adapter path and optional `ADAPTER_REPO` override |
| `export_gguf.sh` | llama.cpp handles all architectures |

## Bleeding-Edge Track Rules

- **Qwen3 4B:** create first if the goal is a strong Hermes agent on 32GB.
- **LFM/LFM2.5:** create first if latency and on-device behavior matter more than broad benchmark score.
- **Qwen3-Next / RecurrentGemma / Mamba / RWKV:** create only after a runtime proof. These are architecture experiments, so do not assume GGUF, MLX, Ollama, and LM Studio all work.
- **LFM2-24B-A2B:** treat as inference/runtime research on 32GB, not a first fine-tune target.
