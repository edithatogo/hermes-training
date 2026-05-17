# Adding a New Model — Conductor Workflow

## 1-Minute Checklist

Changing from Gemma 4 to a new model requires touching exactly **3 files:**

```bash
# 1. Create new repo from template
cp -r /Users/doughnut/GitHub/hermes-training/gemma4 /Users/doughnut/GitHub/hermes-training/{new-model}

# 2. Change the MODEL ID in the training config
sed -i '' 's|google/gemma-4-E4B-it|huggingface/{model-id}|' {new-model}/scripts/train_config.yaml

# 3. Write a model-specific Modelfile
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
| GGUF conversion | `llama.cpp` handles any HF model | `export_ollama.sh` |
| Ollama packaging | Modelfile is model-specific, rest is identical | `export_ollama.sh` |

## Creating a New Model Track

```bash
# Run this from the hub:
cd /Users/doughnut/GitHub/hermes-training

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

# 8. Export
bash scripts/export_ollama.sh experiments/{adapter-dir} {model-name}-hermes
```

## What Must Change Per Model

Only these parts are model-specific:

| Component | Why It Differs | Example |
|-----------|---------------|---------|
| `train_config.yaml:model` | Different HuggingFace ID | `google/gemma-4-E4B-it` → `google/recurrentgemma-2b-it` |
| `Modelfile TEMPLATE` | Different chat template format | Gemma: `<\|start_header_id\|>` → LFM2: `<\|im_start\|>` → Gemma/RecurrentGemma: `<start_of_turn/>` |
| `Modelfile FROM` | Different base model or GGUF path | `FROM google/gemma-4-E4B-it` → `FROM google/recurrentgemma-2b-it` |
| `train_config.yaml:batch_size` | Memory varies by model size | 4B model: batch 4 → 9B model: batch 2 |
| `CONDUCTOR.md` | Track updates | Model name, license, status |

## What Stays Identical Across Models

| Component | Why It's the Same |
|-----------|------------------|
| `build_dataset.py` | Data format is model-agnostic (JSONL messages) |
| `train.py` | mlx-lm handles all HuggingFace transformers |
| `evaluate.py` | Works with any model loaded via mlx_lm |
| `compare.py` | Compares any two models |
| `download_hermes_dataset.py` | Sources same Hermes data, format is universal |
| `export_ollama.sh` | Generic script, only needs adapter path + model name |
| `push_to_hf.sh` | Generic, only needs adapter path |
| `export_gguf.sh` | llama.cpp handles all architectures |
