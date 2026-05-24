# Hermes Training Hub

Bleeding-edge model lab for adapting, benchmarking, packaging, and publishing Hermes-agent models across local and cloud-assisted platform lanes.

The MacBook Pro M1 Max/MLX setup is the first constrained local lane, not the product boundary. The hub is intentionally platform- and runtime-aware:

- **Train locally where realistic:** MLX LoRA on Apple Silicon.
- **Scale when useful:** Azure GPU for benchmarks, teacher/evaluator runs, and selected larger experiments after preflight.
- **Serve fast on Mac:** MLX runtime or Ollama's experimental safetensors/MLX path when the local Ollama build supports it.
- **Serve broadly:** GGUF export for Ollama and LM Studio.
- **Explore specialist runtimes:** KTransformers, RWKV7, BitNet, Mamba-family SSMs, and experimental recursive checkpoints only after runtime proof.
- **Use with Hermes:** prefer `ollama launch hermes`, which configures Hermes against Ollama's OpenAI-compatible endpoint.
- **Publish:** GitHub for code, Hugging Face for datasets/adapters/model cards.

## Current Tracks

```
hermes-training/
├── gemma4/          -> Gemma/Gemma4-family LoRA track
├── lfm2/            -> LFM/LFM2/Ministral experimental track
├── mem0/            -> mem0 extraction, memory retrieval, and embedding adaptation track
└── ollama-pack/     -> Ollama and GGUF packaging scripts
```

The nested track directories are separate Git repos. The hub is the orchestrator and should either keep them as documented external repos or convert them to real submodules before relying on `git submodule`.

Conductor planning now lives in structured `conductor/` directories:

- Hub: [conductor/index.md](./conductor/index.md)
- Health target: [conductor/health-score.md](./conductor/health-score.md)
- LFM track: [lfm2/conductor/index.md](./lfm2/conductor/index.md)
- Gemma/Qwen/Hermes track: [gemma4/conductor/index.md](./gemma4/conductor/index.md)
- mem0 memory and embedding track: [mem0/README.md](./mem0/README.md)
- Runtime track: [ollama-pack/conductor/index.md](./ollama-pack/conductor/index.md)

## Priority Roadmap

| Priority | Family | Candidate | Why | Preferred runtime |
|---|---|---|---|---|
| 1 | Qwen | `Qwen/Qwen3.6-35B-A3B` | Current open-weight frontier agent/coder; 35B total, 3B active | KTransformers, Ollama/LM Studio GGUF, Transformers |
| 2 | Hermes | `NousResearch/Hermes-4-14B`, `NousResearch/Hermes-4.3-36B` | Hermes-aligned baselines; 4.3-36B is newer public Hermes, 14B is the smaller first baseline | Ollama/LM Studio GGUF, Transformers |
| 3 | Gemma | `google/gemma-4-26B-A4B-it` | 26B MoE, 4B active, multimodal and agentic | Ollama/LM Studio GGUF, MLX if supported |
| 4 | Qwen small | `Qwen/Qwen3-4B-MLX-4bit` | Strong low-risk fine-tune target that fits 32GB comfortably | MLX, Ollama experimental, GGUF |
| 5 | LFM | `LiquidAI/LFM2.5-350M`, `LiquidAI/LFM2.5-1.2B-Instruct`, `LiquidAI/LFM2.5-1.2B-Thinking`, `LiquidAI/LFM2-8B-A1B` | Hybrid/on-device models, fast active parameter count | LEAP/Unsloth/TRL for LFM2.5, Ollama/GGUF |
| 6 | Research runtime | Qwen3-Next, Mamba-3, `BlinkDL/rwkv7-g1`, `microsoft/bitnet-b1.58-2B-4T`, `mit-oasys/rlm-qwen3-8b-v0.1` | Linear/recurrent/ternary/recursive architecture experiments | Experimental; validate runtime support first |

See [PROJECT_LAYOUT.md](./PROJECT_LAYOUT.md) for the high-level lane map, [PLATFORM_LANES.md](./PLATFORM_LANES.md) for the platform abstraction, [MODEL_CANDIDATES.yaml](./MODEL_CANDIDATES.yaml) for the machine-readable Hermes/chat radar, [mem0/MODEL_CANDIDATES.yaml](./mem0/MODEL_CANDIDATES.yaml) for memory/extraction/embedding candidates, [FUTURE_MODELS.md](./FUTURE_MODELS.md) for model notes, [FRAMEWORKS.md](./FRAMEWORKS.md) for framework choices, [AZURE_SCALEOUT.md](./AZURE_SCALEOUT.md) for cloud acceleration, and [RUNTIME_TARGETS.md](./RUNTIME_TARGETS.md) plus [mem0/RUNTIME_TARGETS.md](./mem0/RUNTIME_TARGETS.md) for runtime rules.

The remaining work is now split into parallel Conductor lanes in [PARALLEL_ROADMAP.md](./PARALLEL_ROADMAP.md). The current model-release scan is recorded at [reports/model-radar/current-release-scan-20260524.md](./reports/model-radar/current-release-scan-20260524.md).

Use [BENCHMARKING_PLAN.md](./BENCHMARKING_PLAN.md) to decide whether an adapter is actually better than the base model. Use [mem0/BENCHMARKS.md](./mem0/BENCHMARKS.md) for memory, embedding, retrieval, and reranking benchmarks. Use [STANDARD_BENCHMARKS.md](./STANDARD_BENCHMARKS.md) for standardized benchmarks that should accompany GitHub/Hugging Face publication. Use [DOCUMENTATION_PLAN.md](./DOCUMENTATION_PLAN.md) before publishing adapters or datasets. Use [APPLICATIONS.md](./APPLICATIONS.md) to decide which model family fits each downstream use.

## Pipeline

Each model track should follow the same promotion gates:

```
dataset profile -> smoke train -> eval -> publish adapter -> package runtime -> Hermes validation
```

Recommended dataset profiles:

| Profile | Use | Approx size |
|---|---|---|
| `smoke` | Validate downloader, tokenizer, trainer, export | 500-1,000 conversations |
| `pilot` | First meaningful behavior check | 10k-25k conversations |
| `full` | Publishable adapter candidate | 50k-150k conversations |

Current checked-in data is smoke-test scale, not a publishable fine-tune.

mem0 and embedding work uses a related but separate promotion pipeline:

```
candidate model -> isolated collection/index -> add/search smoke -> recency and distractor eval -> latency check -> runtime card -> optional default promotion
```

The current mem0 default remains `nomic-embed-text:latest` with Qdrant collection `mem0_nomic_768`; new embedding models must use a separate collection when dimensions or index shape differ.

## Environment

Use a Python 3.11+ virtual environment with MLX tooling:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Keep model caches off the internal disk:

```bash
source scripts/env.sh
```

`scripts/env.sh` defaults `HF_HOME`, `HF_HUB_CACHE`, `TMPDIR`, `XDG_CACHE_HOME`, and `PIP_CACHE_DIR` to `/Volumes/PortableSSD` when that volume is present. Override `HERMES_STORAGE_ROOT` for a different external disk.

## Running a Track

Example:

```bash
./lfm2/scripts/run_train.sh scripts/train_config.lfm25-1.2b-instruct.smoke.yaml
./gemma4/scripts/run_train.sh scripts/train_config.qwen3-4b.smoke.yaml
```

The track launchers source the shared environment helper, accept extra `train.py` flags such as `--dry-run`, and keep paths relative to the repo location.

Current smoke proof:

- `LiquidAI/LFM2.5-1.2B-Instruct` completed a 10-iteration MLX LoRA smoke run on the M1 Max, saved adapters under `lfm2/experiments/lfm25-1.2b-instruct-smoke/lora_adapter`, and peaked at about 3.6 GB.
- `Qwen/Qwen3-4B-MLX-4bit` is configured but its initial unauthenticated Hugging Face download stalled; retry with a valid `HF_TOKEN` or prefetch it before treating it as ready.

Audit dataset tokens:

```bash
source scripts/env.sh
HF_HUB_OFFLINE=1 ./.venv/bin/python scripts/dataset_token_audit.py \
  --model LiquidAI/LFM2.5-1.2B-Instruct \
  --data lfm2/data/splits
```

## Hermes Runtime Paths

Best default:

```bash
ollama launch hermes
```

Ollama's Hermes launcher configures Hermes to use the local Ollama OpenAI-compatible endpoint at `http://127.0.0.1:11434/v1`.

Fallbacks:

- MLX server: `mlx_lm.server --model <model-or-adapter>` then point Hermes at that OpenAI-compatible endpoint.
- Ollama GGUF: create a model from a `Modelfile`, then launch Hermes through Ollama.
- LM Studio: load the GGUF and point Hermes at LM Studio's OpenAI-compatible local server.
- Normalizing proxy: for Qwen-family outputs, point Hermes at `http://127.0.0.1:8099/v1` after starting `scripts/openai_normalizing_proxy.py` in front of Ollama, MLX server, or LM Studio. The proxy removes only empty leading `<think></think>` wrappers and rejects streaming responses.

## Publication Status

GitHub remotes exist for the hub and current tracks. Hugging Face repos are planned and should be created by the updated `push_to_hf.sh` scripts only after adapters and dataset cards exist.

Adapter publication also requires a strict `1.000` pass on the held-out local tool-call suite at `benchmarks/tool_call_local/heldout_suite.json`. The mirrored suite at `benchmarks/tool_call_local/suite.json` overlaps the current strict seed and is only a regression check.

Planned Hugging Face repos:

| Repo | Contents |
|---|---|
| `edithatogo/hermes-training-data` | Shared JSONL train/val/test dataset |
| `edithatogo/gemma4-e4b-hermes-lora` | Gemma-family LoRA adapter |
| `edithatogo/lfm2-8b-hermes-lora` | LFM2 LoRA adapter |
| `edithatogo/ministral-8b-hermes-lora` | Ministral LoRA adapter |
| `edithatogo/qwen3-4b-hermes-lora` | Qwen3 LoRA adapter |

## Maintenance

```bash
scripts/repo_status.sh
./.venv/bin/python scripts/validate_readiness.py
python3 scripts/check_model_candidates.py
python3 scripts/check_mem0_model_candidates.py
```

See [REPO_MAINTENANCE.md](./REPO_MAINTENANCE.md) before committing or publishing.
