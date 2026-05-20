# Fine-Tuning And Runtime Frameworks

This workspace is Hermes-agent-first. Mac/MLX is the constrained local lane, but framework choice follows model role, platform lane, and runtime proof.

## Decision Matrix

| Framework / SDK | Use For | Mac M1 Max Fit | Status In This Project | Notes |
|---|---|---|---|---|
| MLX-LM | Qwen3 4B, Gemma edge, small/medium adapters | Best | Primary | Use for local SFT LoRA first. |
| mlx-tune | Unsloth-like API on MLX | Promising | Watch/adopt after smoke test | Useful if it reduces friction for SFT/DPO/GRPO on Mac. |
| Unsloth | LFM2.5 recipes, CUDA/HF Jobs workflows | Not native Mac unless MLX-compatible wrapper is used | Secondary/cloud | Official LFM2.5 card links Unsloth recipes, but standard Unsloth depends on CUDA/Triton. |
| Azure ML | Benchmark, teacher/evaluator, and selected larger experiment orchestration | Not local | Cloud lane | Requires Gmail student account login, Azure ML extension, quota, and cost preflight. |
| KTransformers | Qwen MoE inference/fine-tuning experiments | Verify | Experimental | Qwen3.6 official card names KTransformers, but local Apple Silicon support must be proven before relying on it. |
| LEAP / leap-finetune | Liquid LFM2/LFM2.5 tuning | Verify | Experimental LFM path | Liquid docs position `leap-finetune` for LFM2 fine-tuning; confirm local backend before committing. |
| TRL / PEFT | Generic SFT/DPO/GRPO | Possible via MPS/CPU, often slower | Secondary | Useful when MLX support is missing. |
| RWKV-LM | RWKV recurrent models | Verify | Research | Use only after runtime/tool-call smoke tests. |
| BitNet/QVAC/BitLoRA | Ternary model experiments | Research | Watchlist | Do not block Hermes roadmap on this. |

## Recommended Stack By Model

| Model | First Runtime | First Fine-Tune Attempt | Publication Strategy |
|---|---|---|---|
| Qwen3 4B | MLX | MLX-LM LoRA | Adapter + optional GGUF |
| Qwen3.6-35B-A3B | LM Studio/Ollama GGUF or KTransformers | Defer; try adapter only after memory smoke | Adapter-only if trained |
| Hermes-4-14B | Ollama/LM Studio GGUF | Defer; use as baseline/teacher first | Do not publish derivative until license reviewed |
| Gemma 4 26B-A4B | Ollama/LM Studio GGUF | Defer; strict low-memory smoke first | Adapter-only |
| LFM2.5 1.2B | MLX or GGUF | LEAP/Unsloth/TRL/MLX depending on support | Adapter + GGUF when license permits |
| LFM2 8B-A1B | Ollama/GGUF | MLX or LEAP after runtime proof | Adapter-only initially |
| Mamba-3 | Research runtime | Defer | No publish path yet |
| RWKV-7 | RWKV runtime | Defer | Adapter/checkpoint only after quality proof |

## Guardrails

- Do not assume "active parameters" means training memory is small. MoE training can still touch routing, optimizer state, KV cache, and full model metadata.
- On 32GB, promote large MoE models as **inference targets first** and **fine-tune targets second**.
- Keep `max_seq_length` small for first training smoke tests: 512-1024 tokens.
- Use batch size 1 for large MoE smoke tests.
- Publish exact base model revision and runtime validation results in every model card.
- Do not move a model from watchlist to training until its platform lane and runtime path are verified.
- Use CUDA-only frameworks in the Azure lane by default; do not force them into the Mac lane.
