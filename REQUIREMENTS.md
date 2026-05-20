# Requirements — Hermes Training Hub

> **Scope:** Adapt, benchmark, serve, and publish Hermes-ready bleeding-edge models across local Mac, cloud, retrieval, and specialist-runtime lanes.
> **Status:** Active scaffold. GitHub exists; Hugging Face publication and trained adapters are not complete yet.

## Must Have

| ID | Requirement | Track | Verification |
|---|---|---|---|
| M1 | Reproducible Apple Silicon environment | hub, all tracks | `python -c "import mlx, mlx_lm"` succeeds inside `.venv` |
| M2 | Real Hermes dataset downloader with configurable size profiles | all training tracks | smoke/pilot/full profile produces non-empty splits |
| M3 | MLX LoRA training pipeline | all training tracks | `scripts/train.py --config ... --dry-run` and a smoke train pass |
| M4 | Adapter artifacts saved outside Git history | all training tracks | `adapters.safetensors` and `adapter_config.json` exist under `experiments/` |
| M5 | Evaluation gate before publish | all training tracks | base-vs-adapter report covers tool calls, JSON, multi-turn, coding, refusal |
| M6 | Hugging Face publication path | all training tracks | `hf upload` publishes adapter card + adapter files to private repo |
| M7 | Tool-agnostic runtime packaging | ollama-pack | at least one path works: MLX server, Ollama safetensors, Ollama GGUF, LM Studio GGUF |
| M8 | Hermes launch validation | ollama-pack | `ollama launch hermes` sees the model through `/v1/models` |
| M9 | GitHub remotes are current | hub, all tracks | `git status -sb` clean and `main...origin/main` has no ahead commits |
| M10 | Model cache uses external SSD | all tracks | `HF_HOME` and `HF_HUB_CACHE` point at `/Volumes/PortableSSD/huggingface` |
| M11 | Platform lanes separate purpose from environment | hub | `PLATFORM_LANES.md` and Conductor docs classify every model path |
| M12 | Azure preflight gates cloud work | hub | `scripts/azure_preflight.py` passes before compute or job submission |

## Should Have

| ID | Requirement | Track | Priority |
|---|---|---|---|
| S1 | Qwen3 4B Hermes track | future/qwen | HIGH |
| S2 | Qwen3.6 35B-A3B runtime track | future/qwen36 | HIGH |
| S3 | Hermes 4 14B baseline/evaluator track | future/hermes4 | HIGH |
| S4 | Gemma 4 26B-A4B runtime track | future/gemma4-26b | HIGH |
| S5 | LFM2/LFM2.5 Hermes track | lfm2 | HIGH |
| S6 | Automated runtime smoke tests for OpenAI-compatible `/v1/chat/completions` | ollama-pack | HIGH |
| S7 | Dataset quality filters for tool-call XML/JSON validity | all training tracks | HIGH |
| S8 | Leaderboard across base vs fine-tuned vs runtime target | hub | MEDIUM |
| S9 | Model cards include exact base revision, dataset profile, commit SHA, eval summary | all training tracks | HIGH |
| S10 | Multiple quantization outputs where runtime supports them | ollama-pack | MEDIUM |
| S11 | KTransformers/LEAP/Unsloth feasibility notes with local smoke results | hub | MEDIUM |
| S12 | Qwen3-Next, Mamba-3, RWKV-7, BitNet research watchlist | future/subquadratic | MEDIUM |
| S13 | Retrieval/memory lane for embedding and reranker models | future/retrieval | HIGH |

## Could Have

| ID | Requirement | Track | Value |
|---|---|---|---|
| C1 | Preference tuning after SFT | future | HIGH |
| C2 | DFlash/speculative decoding runtime notes where Ollama MLX supports them | ollama-pack | MEDIUM |
| C3 | LM Studio import metadata for GGUF builds | ollama-pack | MEDIUM |
| C4 | Private HF dataset version tags per dataset profile | hub | MEDIUM |
| C5 | Automated nightly model radar from Hugging Face API | hub | LOW |

## Won't Have For This Iteration

| ID | Requirement | Reason |
|---|---|---|
| W1 | Full pretraining from scratch | Not feasible on one M1 Max. |
| W2 | Unguarded CUDA/ROCm training | Use Azure/CUDA only after account, quota, and cost preflight. |
| W3 | Treating large models as local fine-tune targets by default | Use runtime, teacher, or cloud lanes until memory proof exists. |
| W4 | Treat smoke-test adapters as publishable models | They validate plumbing only. |
| W5 | Assume every experimental architecture is Ollama/LM Studio ready | Runtime support must be verified per architecture. |

## Current Gap Summary

- `mlx_lm` is not installed in the current shell, so training dry-runs fail until the environment is bootstrapped.
- Current data splits are smoke scale, roughly 460 training conversations per model.
- No local adapter artifacts were found under `experiments/`.
- Hugging Face repos are not created yet.
- The hub has nested Git repos but no `.gitmodules`; do not rely on `git submodule` until this is resolved.
