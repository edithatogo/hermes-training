# Hermes Training Hub

Multi-model Hermes-style fine-tuning workspace for MacBook Pro M1 Max (32GB).

## Structure

```
hermes-training/
├── gemma4/          → Gemma 4 E4B-it LoRA fine-tune (in progress)
├── lfm2/            → LFM2-8B-A1B LoRA fine-tune (scaffolded)
└── ollama-pack/     → Ollama Modelfiles and packaging scripts
```

## Workflow

Each model repo follows the same pipeline:

```
raw data → build_dataset → train (MLX LoRA) → eval → export → Ollama
```

## Prerequisites

- **Python 3.11+** with `mlx`, `mlx-lm`, `datasets`, `huggingface_hub`
- **llama.cpp** at `/Users/doughnut/GitHub/llama.cpp` (for GGUF conversion)
- **Ollama** installed and running
- **Portable SSD** at `/Volumes/PortableSSD/` for model caches (750GB free)
- **GitHub** auth (gh CLI logged in)

## Running a Full Pipeline

```bash
# 1. Download dataset
cd gemma4
python3 scripts/download_hermes_dataset.py

# 2. Train
python3 scripts/train.py --config scripts/train_config.yaml

# 3. Evaluate
python3 scripts/evaluate.py --model google/gemma-4-E4B-it --adapter experiments/gemma4-e4b/lora_adapter --prompts eval/prompts.jsonl --report eval/report.html

# 4. Compare base vs fine-tuned
python3 scripts/compare.py \
  --base-model google/gemma-4-E4B-it \
  --ft-model google/gemma-4-E4B-it \
  --ft-adapter experiments/gemma4-e4b/lora_adapter \
  --prompts eval/prompts.jsonl \
  --output eval/comparison.html

# 5. Export to Ollama
bash scripts/export_ollama.sh experiments/gemma4-e4b/lora_adapter gemma4-hermes

# 6. Push to HuggingFace
bash scripts/push_to_hf.sh experiments/gemma4-e4b/lora_adapter
```

## Model Comparison

| Model | Params | Active | Size | Status |
|-------|--------|--------|------|--------|
| Gemma 4 E4B-it | 4B | 4B | ~16GB | Training in progress |
| LFM2-8B-A1B | 8B | 1B | ~4GB | Scaffolded |

## GitHub Repos

| Repo | URL | Status |
|------|-----|--------|
| hermes-gemma-lab | github.com/edithatogo/hermes-gemma-lab | Active training |
| hermes-lfm2-lab | github.com/edithatogo/hermes-lfm2-lab | Dataset downloading |
| hermes-ollama-pack | github.com/edithatogo/hermes-ollama-pack | Packaging scripts |

## HuggingFace Repos (planned)

| Repo | Contents |
|------|----------|
| edithatogo/hermes-training-data | Shared training dataset (JSONL) |
| edithatogo/gemma4-e4b-hermes-lora | Gemma 4 LoRA adapter + model card |
| edithatogo/lfm2-8b-hermes-lora | LFM2 LoRA adapter + model card |

## Conductor Notes

Each subrepo has a `CONDUCTOR.md` for context preservation. Load these skills:
- `kanban-orchestrator` for task decomposition
- `kanban-worker` for implementation context
- `writing-plans` for detailed implementation planning
