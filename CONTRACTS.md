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

## Contract 2A: Strict Tool-Call Seed Lane

**Producer:** manual curation, benchmark mirroring, or lane-specific build jobs
**Consumer:** strict tool-call training runs, validation splits, local benchmark alignment

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
- The seed lane is a curated subset of chat JSONL examples, isolated from the general `data/raw/` and `data/splits/` corpora
- The system prompt must define the candidate tools and instruct the model to return only `<tool_call>` blocks for valid cases
- Valid tool targets must contain only exact `<tool_call>` blocks, one per tool call, with no surrounding prose
- Invalid-tool examples may use plain text refusal or clarification and must not fabricate an unavailable tool
- Multi-turn repair examples may include a malformed assistant turn followed by a correction turn
- Split policy is deterministic: sort by `id`, take 80% for train, 10% for val, and the remainder for test
- For the checked-in 10-example seed, that yields 8 train examples, 1 validation example, and 1 test example
- Generated training, evaluation, and export artifacts MUST live on SSD-backed storage under `$HERMES_STORAGE_ROOT`, `$HERMES_EVAL_ROOT`, or `$HERMES_EXPORT_ROOT`
- Only the tiny seed JSONL and documentation/contracts are checked in; build outputs and caches must not be committed

**File location:** `gemma4/data/strict_tool_call/{raw,splits}/...`

**Contract ID:** DATA-STRICT-TOOLCALL-001

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

## Contract 3A: Model Radar Platform Entry

**Producer:** `MODEL_CANDIDATES.yaml`
**Consumer:** Conductor tracks, benchmark plans, runtime packaging

Every model entry must declare `role`, `environment`, and `feasibility` so local Mac work remains constrained and cloud/specialist work is explicit.

Allowed roles:

- `local-finetune`
- `local-runtime`
- `cloud-teacher`
- `cloud-finetune`
- `retrieval`
- `research-runtime`
- `watchlist`

Allowed environments:

- `mac-mlx`
- `mac-ollama`
- `mac-lmstudio`
- `azure-cuda`
- `hf-transformers`
- `retrieval`
- `specialist-runtime`

Watchlist or speculative entries cannot be used for training or publication claims until promoted.

**Contract ID:** MODEL-RADAR-001

---

## Contract 3B: Azure Scale-Out Preflight

**Producer:** `scripts/azure_preflight.py`
**Consumer:** Azure benchmark/training tracks

Before any Azure compute or job submission:

- active user must match the intended Azure account unless overridden
- subscription must be enabled
- Azure ML CLI extension must be present
- SSD artifact root must exist
- cost policy must be recorded as Spot/low-priority, max one GPU job, scale to zero by default

**Contract ID:** AZURE-PREFLIGHT-001

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

## Contract 5A: Retrieval Contrastive JSONL

**Producer:** retrieval dataset curation or retriever mining jobs
**Consumer:** retriever training, hard-negative mining, offline similarity checks

**Schema:**
```json
{
  "id": "string (unique identifier)",
  "anchor": {
    "id": "string",
    "text": "string",
    "source_id": "string",
    "chunk_id": "string (optional)"
  },
  "positive": {
    "id": "string",
    "text": "string",
    "source_id": "string",
    "chunk_id": "string (optional)"
  },
  "negatives": [
    {
      "id": "string",
      "text": "string",
      "source_id": "string",
      "chunk_id": "string (optional)",
      "hard_negative": "boolean (optional, default: true)"
    }
  ],
  "metadata": {
    "domain": "string",
    "scenario": "string",
    "split": "string (one of: train, val, test)",
    "language": "string (optional)"
  }
}
```

**Constraints:**
- Each JSONL line is exactly one triplet-style retrieval example
- `anchor.text` and `positive.text` must not be identical
- `negatives` must contain at least 1 item
- At least one negative SHOULD be a hard negative when available
- Anchors must be query-like; positives must be the retrieved target passage or passage span
- Do not include chat-role transcripts or assistant turns in this file
- Do not mix labels from different retrieval tasks in a single line unless the `metadata.scenario` explicitly describes a multi-task example
- Examples must be chunked before serialization if the source passage exceeds the model context window

**File location:** `data/retrieval/{train,val,test}.jsonl`

**Contract ID:** RETRIEVAL-JSONL-001

---

## Contract 5B: Hermes Memory and RAG Eval Scenarios

**Producer:** benchmark curation, manual test authoring, or scenario synthesis jobs
**Consumer:** retriever eval harnesses, Hermes memory regression tests, run cards

**Schema:**
```json
{
  "id": "string (unique identifier)",
  "scenario": "string (one of: memory_recall, doc_grounded_qa, multi_hop_retrieval, preference_update, recency_conflict, source_attribution, tool_state_recall, distractor_resistance)",
  "query": "string",
  "context": [
    {
      "id": "string",
      "text": "string",
      "kind": "string (one of: gold, distractor, hard_negative, prior_memory)"
    }
  ],
  "expected": {
    "answer_summary": "string",
    "required_citations": ["string"],
    "must_use_context": "boolean"
  },
  "metadata": {
    "split": "string (one of: train, val, test)",
    "source": "string",
    "language": "string (optional)"
  }
}
```

**Constraints:**
- Each scenario must test retrieval or memory grounding, not open-ended chat fluency
- Every scenario must include at least 1 gold context item and at least 1 distractor or hard negative when relevant
- `required_citations` must name the source ids expected in a grounded answer
- `must_use_context` SHOULD be true for grounded memory and RAG checks
- Scenario sets must include recency-sensitive cases where a newer memory overrides an older one
- Scenario sets must include at least one multi-hop case and one source-attribution case before publication claims are made

**Contract ID:** RETRIEVAL-EVAL-001

---

## Contract 5C: MTEB and Retrieval Benchmark Command Shape

**Producer:** benchmark scripts or run-card generation
**Consumer:** local evaluation runs, publication reports, model cards

**Shape:**
```bash
source scripts/env.sh
mteb run \
  -m <model_id_or_path> \
  -t "<retrieval_task_or_benchmark>" \
  --output-folder "$HERMES_EVAL_ROOT/mteb/<run-id>"
```

**Constraints:**
- The command must target retrieval or embedding tasks only when run for the retrieval lane
- Record the exact `mteb` version, model revision, task list, and output folder in the run card
- Limited-sample or engineering runs must be labeled as such and must not be published as benchmark scores
- If a custom task filter is needed, the Python API may use `mteb.get_tasks(task_types=["Retrieval"])`

**Contract ID:** RETRIEVAL-MTEB-001

---

## Contract 5D: Local Vector Store and Retriever Serving Shape

**Producer:** retriever indexing jobs and local serving wrappers
**Consumer:** Hermes runtime, local memory/RAG tests, publication run cards

**Decision:**
- Default local store: SSD-backed FAISS index for dense retrieval plus SQLite metadata for corpus lineage and chunk provenance
- Late-interaction models such as ColBERT may use their own on-disk index artifacts, but they MUST present the same retriever API
- Indexes must be rebuildable from the corpus manifest and model hash

**Service shape:**
```http
GET /health
POST /retrieve
```

**`POST /retrieve` request:**
```json
{
  "query": "string",
  "top_k": 5,
  "mode": "string (one of: dense, hybrid, late_interaction)",
  "filters": {
    "source_ids": ["string"]
  }
}
```

**`POST /retrieve` response:**
```json
{
  "query": "string",
  "index_id": "string",
  "model_id": "string",
  "latency_ms": 0,
  "results": [
    {
      "rank": 1,
      "doc_id": "string",
      "chunk_id": "string",
      "source_id": "string",
      "score": 0.0,
      "text": "string",
      "citation": "string"
    }
  ]
}
```

**Constraints:**
- The service MUST return citation-ready ids for every retrieved item
- The service MUST be deterministic for a fixed corpus manifest, model hash, and index hash
- Hermes must call retrieval as a separate tool/service step, not through chat SFT adapters
- The retriever MUST expose a simple health check so smoke tests can verify the index is loaded

**Contract ID:** RETRIEVER-SERVICE-001

---

## Contract 5E: Retriever Card Publication Guidance

**Producer:** model cards, dataset cards, run cards, and release notes
**Consumer:** GitHub release pages, Hugging Face cards, human reviewers

**Required publication fields:**
- retriever role and lane
- model family and revision
- index type and rebuild command
- corpus provenance and license notes
- benchmark commands and task list
- retrieval metrics such as Recall@k, nDCG@10, and MRR@10 where applicable
- latency and throughput notes
- known limitations and unsupported corpus types

**Constraints:**
- Publish code, configs, benchmark definitions, run cards, and small summary tables
- Do not publish raw private corpora, user prompts, or proprietary embeddings
- Do not claim chat SFT gains from a retriever card
- State clearly whether the artifact is a dense encoder, reranker, or late-interaction retriever
- The card must match the corpus digest and index hash used for the published numbers

**Contract ID:** RETRIEVER-CARD-001

---

## Contract 5F: Local Tool-Call Benchmark Suite and Scorecard

**Producer:** `benchmarks/tool_call_local/suite.json`, `benchmarks/tool_call_local/heldout_suite.json`, `scripts/run_tool_call_benchmark.py`
**Consumer:** Hermes-local benchmark runs, run cards, publication notes

**Suite schema:**
```json
{
  "id": "string (unique identifier)",
  "category": "string (one of: json_validity, argument_correctness, invalid_tool_handling, multi_turn_repair)",
  "messages": [
    {
      "role": "string (one of: system, user, assistant)",
      "content": "string"
    }
  ],
  "expected": {
    "mode": "string (one of: tool_calls, text)",
    "tool_calls": [
      {
        "name": "string",
        "arguments": {}
      }
    ],
    "must_contain_any": ["string"],
    "must_not_have_tool_calls": "boolean"
  }
}
```

**Constraints:**
- The suite must contain at least one case for each required category: JSON validity, argument correctness, invalid-tool handling, and multi-turn repair
- Tool-call cases must use exact JSON tool-call expectations
- Invalid-tool handling cases must not hallucinate unavailable tools and should contain a refusal or clarification marker
- Multi-turn repair cases must include prior malformed assistant context or an explicit correction turn
- `suite.json` may overlap strict training seed data and is a regression suite only
- `heldout_suite.json` must not overlap the benchmark-mirrored strict training seed and is the strict local publication gate
- The runner must write raw outputs and summaries under `$HERMES_EVAL_ROOT/tool-call-benchmark/<run-id>` unless an explicit `--output-dir` is supplied
- Published scores must retain the exact suite revision, model revision, and runner command used to produce them
- Adapter publication requires strict `1.000` pass rate on `heldout_suite.json`; diagnostic normalization metrics cannot replace this gate

**Results schema:**
```json
{
  "id": "string",
  "category": "string",
  "response": "string",
  "latency_s": "float|null",
  "json_valid": "boolean",
  "tool_name_valid": "boolean",
  "arguments_correct": "boolean|null",
  "pass": "boolean"
}
```

**Contract ID:** TOOLCALL-BENCH-001

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
