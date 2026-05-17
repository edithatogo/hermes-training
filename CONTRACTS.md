# Contracts — Hermes Training Hub Interface Specifications

> **Purpose:** Define the exact interfaces between pipeline stages so each component can be developed, tested, and replaced independently.
> **Status:** Active
> **Version:** 1.0

---

## Contract 1: Data Format — RAW JSONL

**Producer:** `download_hermes_dataset.py`
**Consumer:** `build_dataset.py`

**Schema:**
```json
{
  "id": "string (unique identifier)",
  "messages": [
    {
      "role": "string (one of: system, user, assistant)",
      "content": "string (message text)"
    }
  ]
}
```

**Constraints:**
- Each JSONL line is exactly one JSON object
- `id` must be unique within the file
- `messages` array must have at least 2 entries
- `role` must be one of: `system`, `user`, `assistant`
- `role` must not appear twice consecutively
- The first message may be `system` (optional)
- After loading, producer MUST generate at least 100 conversations
- Contracts SHALL be versioned in the `id` field prefix (e.g., `hermes3-dataset-0`)

**File location:** `data/raw/{source_name}.jsonl`

**Contract ID:** DATA-RAW-001

---

## Contract 2: Data Format — SPLIT JSONL

**Producer:** `build_dataset.py`
**Consumer:** `train.py`

**Schema:**
```json
{
  "id": "string (unique identifier)",
  "messages": [
    {
      "role": "string (one of: system, user, assistant)",
      "content": "string (message text)"
    }
  ]
}
```

**Constraints:**
- Same schema as DATA-RAW-001
- All conversations deduplicated (SHA256 hash of concatenated role:content)
- Conversations with fewer than `--min-turns` or more than `--max-turns` filtered out
- Split ratios: 80% train, 10% val, 10% test (configurable via CLI)
- Each split file must contain at least 1 conversation
- Files named: `train.jsonl`, `val.jsonl`, `test.jsonl`

**File location:** `data/splits/{train,val,test}.jsonl`

**Contract ID:** DATA-SPLIT-001

---

## Contract 3: Training Configuration

**Producer:** `train_config.yaml` (manual)
**Consumer:** `train.py`

**Schema (YAML):**
```yaml
model: string                    # HuggingFace model ID (required)
adapter_path: string             # Output directory for LoRA weights
data: string                     # Path to data/splits/ directory
lora_rank: integer               # LoRA rank (default: 16)
lora_scale: float                # LoRA scale (default: 20.0)
lora_dropout: float              # LoRA dropout (default: 0.0)
lora_layers: integer             # Number of layers to adapt (default: 16)
batch_size: integer              # Per-device batch size (default: 4)
iters: integer                   # Training iterations (default: 100)
val_batches: integer             # Validation batches per eval (default: 25)
steps_per_report: integer        # Log frequency (default: 10)
steps_per_eval: integer          # Eval frequency (default: 200)
steps_per_save: integer          # Checkpoint frequency (default: 100)
max_seq_length: integer          # Max token sequence length (default: 2048)
learning_rate: float             # AdamW learning rate (default: 1e-4)
grad_checkpoint: boolean         # Gradient checkpointing (default: false)
grad_accumulation_steps: integer # Gradient accumulation (default: 1)
seed: integer                    # Random seed (default: 42)
```

**Constraints:**
- `model` must be a valid HuggingFace model ID loadable by `mlx_lm.load()`
- `adapter_path` will be created if it doesn't exist
- `data` should point to a directory containing `train.jsonl`
- `iters` should be >= 1
- `batch_size` on M1 Max 32GB must be <= 8 for 4B models, <= 4 for 8B models
- `max_seq_length` on M1 Max 32GB must be <= 2048 for 8B models

**Contract ID:** CFG-TRAIN-001

---

## Contract 4: LoRA Adapter Output

**Producer:** `train.py`
**Consumer:** `export_ollama.sh`, `evaluate.py`

**Files:**
```
{adapter_path}/
├── adapters.safetensors    # LoRA weight matrices
└── adapter_config.json     # Training configuration
```

**adapter_config.json schema:**
```json
{
  "model": "string (base model ID)",
  "lora_rank": "integer",
  "lora_scale": "float",
  "lora_dropout": "float",
  "lora_layers": "integer",
  "max_seq_length": "integer",
  "learning_rate": "float",
  "batch_size": "integer",
  "iters": "integer",
  "seed": "integer"
}
```

**Constraints:**
- `adapters.safetensors` must be loadable by `mlx_lm.load(..., adapter_path=path)`
- `adapter_config.json` must contain at minimum `model` and `lora_rank`
- The base model specified in `model` must be accessible (local cache or HuggingFace)

**Contract ID:** OUT-ADAPTER-001

---

## Contract 5: Evaluation Input

**Producer:** `eval/prompts.jsonl` (manual), `evaluate.py` (results)
**Consumer:** `compare.py`, human inspection

**Prompts schema (input):**
```json
{
  "prompt": "string (the prompt text)",
  "category": "string (one of: explanation, code, comparison, tool_use, debugging, transformation, procedural, factual, discussion, data_science)"
}
```

**Results schema (output):**
```json
{
  "prompt": "string",
  "category": "string",
  "response": "string (model output)",
  "latency_s": "float (generation time in seconds)",
  "response_length": "integer (word count)"
}
```

**Constraints:**
- Input must have at least 10 prompts across at least 5 categories
- Output records maintain 1:1 correspondence with input prompts
- `latency_s` must be measured from model call to response received (not including tokenization)

**Contract ID:** EVAL-001

---

## Contract 6: Ollama Modelfile

**Producer:** `export_ollama.sh`, manual editing
**Consumer:** `ollama create`

**Format:**
```dockerfile
# {model_name} — Ollama Modelfile
# Generated from {source_repo}

FROM {gguf_file_path}

SYSTEM """{system_prompt}"""

TEMPLATE """{chat_template}"""

PARAMETER temperature {float}
PARAMETER top_p {float}
PARAMETER stop "{stop_token}"
PARAMETER num_ctx {integer}
```

**Constraints:**
- `FROM` must reference a valid GGUF file path (local file or `ollama pull`-able model)
- `TEMPLATE` must match the base model's chat template format
- Modelfiles are NOT JSON — standard Ollama Modelfile syntax
- At least `FROM` and `SYSTEM` directives are REQUIRED
- `TEMPLATE` is REQUIRED for Hermes-style behavior (ensures tool-call formatting)

**File location:** `modelfiles/{ModelName}.Modelfile`

**Contract ID:** MODFILE-001

---

## Contract 7: HuggingFace Adapter Repo

**Producer:** `push_to_hf.sh`
**Consumer:** HuggingFace Hub users

**Repository structure:**
```
{repo_name}/
├── adapters.safetensors    # LoRA weights
├── adapter_config.json     # Training config
└── README.md               # Model card (from exports/hf/adapter_card.md)
```

**Constraints:**
- Repo type: `model`
- License must match base model (Apache 2.0 for Gemma 4)
- Model card must include: base_model, license, training details, usage examples
- Dataset link must reference the training data repo

**Contract ID:** PUB-HF-ADAPTER-001

---

## Contract 8: HuggingFace Dataset Repo

**Producer:** `push_to_hf.sh`
**Consumer:** HuggingFace Hub users

**Repository structure:**
```
{repo_name}/
├── train.jsonl    # Training split
├── val.jsonl      # Validation split
├── test.jsonl     # Test split
└── README.md      # Dataset card (from exports/hf/dataset_card.md)
```

**Constraints:**
- Repo type: `dataset`
- Dataset card must include license, format description, and preprocessing steps
- README must document the chat format schema

**Contract ID:** PUB-HF-DATA-001

---

## Contract 9: Hermes Model Picker Entry

**Producer:** Manual config edit / automation script
**Consumer:** Hermes Agent model picker

**Config entry (`~/.hermes/config.yaml`):**
```yaml
model:
  default: {model_name}
  provider: custom:ollama
custom_providers:
  - name: ollama
    base_url: http://127.0.0.1:11434/v1
    api_mode: chat_completions
    model: {model_name}
```

**Verification:**
```bash
hermes model switch {model_name}
# Expected: picker shows {model_name} under custom:ollama provider
```

**Contract ID:** CFG-HERMES-001

---

## Contract 10: Export Pipeline Exit Conditions

**Producer:** `export_ollama.sh`
**Consumer:** User / automation

**Exit codes:**
| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Model deployed to Ollama |
| 1 | Adapter directory not found | Check path |
| 2 | llama.cpp not found | Clone or build |
| 3 | GGUF conversion failed | Check base model weights |
| 4 | Ollama create failed | Check Modelfile syntax |
| 127 | Command not found | Install dependency |

**Contract ID:** EXIT-EXPORT-001
