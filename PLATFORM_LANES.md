# Platform Lanes

Hermes Training Hub is organized around Hermes-agent model capability, not one machine or runtime.

## Lane Matrix

| Lane | Primary Use | First Models | Promotion Gate |
|---|---|---|---|
| Mac/MLX | Achievable local LoRA training and MLX serving | LFM2.5 1.2B, Qwen3 4B | adapter loads, Hermes-local eval, memory stable |
| Mac/Ollama | Daily Hermes serving and model picker integration | LFM2.5 GGUF, Hermes 4 GGUF, Qwen/Gemma GGUFs | OpenAI endpoint smoke and tool-call JSON checks |
| Mac/LM Studio | GGUF fallback and desktop runtime comparison | Hermes 4, Qwen3.6 quantized, Gemma quantized | OpenAI endpoint smoke and latency/memory notes |
| Azure/CUDA | Benchmarks, teacher/evaluator runs, larger experiments | Hermes 4, Qwen3.6, Gemma 4, Qwen3-Next | preflight, quota, cost guard, run card |
| Retrieval | Hermes memory and RAG | LFM2-ColBERT, BGE-M3, Jina/Qwen embeddings | MTEB/retrieval eval, not chat SFT eval |
| Specialist Runtime | Research architectures | RWKV, BitNet, Mamba/subquadratic, recursive wrappers | weights/license/runtime verified, endpoint smoke |

Format-specific rules live in `RUNTIME_FORMAT_LANES.yaml`. A model can be in a Mac or specialist platform lane while still using MLX, PEFT/safetensors, KTransformers, LEAP/LFM, native recurrent/SSM/BitNet, hosted API, or GGUF as its primary format lane.

## Rules

- Local Mac work is constrained to what fits the 32GB M1 Max without swap-heavy runs.
- Azure hours accelerate work only after account, quota, region, and cost guards pass.
- Watchlist models do not get training claims until a real model card, weights, license, and runtime path are verified.
- Every model card and run card must state the platform lane used for training, evaluation, and runtime validation.
