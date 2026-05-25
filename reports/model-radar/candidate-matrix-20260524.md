# Candidate Matrix

Date: 2026-05-24

This matrix turns the current model radar into execution decisions. It is not a benchmark result.

| Candidate | Lane | First Runtime | Decision State | Next Action | Publication State |
|---|---|---|---|---|---|
| `Qwen/Qwen3-4B-MLX-4bit` v4 targeted LoRA | Mac-local fine-tune | MLX local generation/server | publishable narrow adapter candidate | Keep v4 as current strict Hermes tool-call adapter; broader claims need official benchmarks | public adapter approved, dataset separate |
| `LiquidAI/LFM2.5-1.2B-Instruct` | Mac-local fine-tune | MLX / llama.cpp | runtime/load proof only | MLX server smoke passed, but direct eval quality remains non-compliant; use safer recipe only after candidate selection | blocked |
| `LiquidAI/LFM2.5-1.2B-Thinking` | Mac-local fine-tune | MLX / llama.cpp | runtime-proof candidate | Run local Hermes smoke before training | blocked |
| `Qwen/Qwen3.6-27B` | frontier runtime/teacher | Transformers / GGUF / MLX quant | runtime-proof candidate | Check local artifact or approved download plan | blocked |
| `Qwen/Qwen3.6-35B-A3B` | frontier runtime/teacher | llama.cpp GGUF / KTransformers / Transformers | runtime-proven baseline | Keep as comparison/teacher candidate; strict Hermes tool-call score is `0.000` | runtime-only |
| `unsloth/Qwen3.6-27B-UD-MLX-4bit` | Mac-local runtime | MLX | runtime-proof candidate | Estimate memory, then smoke only if SSD/capacity gates pass | blocked |
| `unsloth/Qwen3.6-27B-MTP-GGUF` | Mac-local runtime | LM Studio / Ollama | runtime-proof candidate | LM Studio smoke candidate if artifact is acquired under SSD policy | blocked |
| `unsloth/Qwen3.6-35B-A3B-MTP-GGUF` | Mac-local runtime | LM Studio / Ollama | runtime-proof candidate | LM Studio smoke candidate; likely inference only | blocked |
| `NousResearch/Hermes-4-14B` | Hermes baseline/teacher | llama.cpp GGUF | runtime-proven baseline | Use as Hermes-aligned baseline/teacher; strict held-out score is `0.250` | runtime-only |
| `SandLogicTechnologies/Hermes-4-14B-GGUF` | Hermes baseline/runtime | llama.cpp / LM Studio | runtime-proven locally | Keep as current Hermes 4 14B Q4 baseline and compare against Qwen3.6 | benchmark-only, not publication candidate |
| `NousResearch/Hermes-4.3-36B` | Hermes baseline/teacher | Transformers / GGUF | cloud/runtime candidate | Treat as teacher baseline after runtime proof | blocked |
| `NousResearch/Hermes-4.3-36B-GGUF` | Mac-local runtime | LM Studio / llama.cpp | runtime-proof candidate | Smoke only if local GGUF exists or user approves download | blocked |
| `google/gemma-4-26B-A4B-it` | frontier runtime/teacher | Transformers / GGUF | runtime-proof candidate | Tool-call stability check after runtime proof | blocked |
| `unsloth/gemma-4-26B-A4B-it-GGUF` | Mac-local runtime | LM Studio / Ollama | runtime-proof candidate | GGUF smoke candidate under SSD policy | blocked |
| `nvidia/Gemma-4-26B-A4B-NVFP4` | specialist/cloud runtime | NVIDIA stack | research-runtime candidate | Azure/specialist proof only | blocked |
| `LiquidAI/LFM2-ColBERT-350M` | retrieval | PyLate / sentence-transformers | retrieval candidate | Add retrieval smoke/MTEB-style lane | no chat adapter publication |
| `Qwen/Qwen3-Embedding-4B` | retrieval | sentence-transformers / Transformers | retrieval candidate | Batch/memory smoke before claims | no chat adapter publication |
| `Qwen/Qwen3-Reranker-4B` | retrieval | Transformers reranker | retrieval candidate | Reranker smoke after embedding baseline | no chat adapter publication |
| `BAAI/bge-m3` | retrieval baseline | FlagEmbedding / sentence-transformers | ready baseline | Use as practical retrieval baseline | no chat adapter publication |
| `LiquidAI/LFM2-24B-A2B-GGUF` | efficient LFM runtime | llama.cpp GGUF | runtime-proven baseline | Use as LFM comparison lane; strict held-out score is `0.375` and IFEval/coding pilots are `1.000` | runtime-only |
| `LiquidAI/LFM2-8B-A1B-GGUF` | efficient LFM runtime | llama.cpp / LM Studio | watchlist | Consider only if a smaller LFM runtime is needed after 24B evidence | blocked |
| `XiaomiMiMo/MiMo-V2-Flash` | large MoE research runtime | KTransformers / specialist GGUF / Azure | watchlist | Do not download locally first; test via Azure/specialist quant only after Qwen3.6 and Gemma queues clear | blocked |
| `RWKV/RWKV7-Goose-World3-2.9B-HF` | recurrent research runtime | Transformers / specialist runtime | watchlist | Add after runtime harness proof | blocked |
| `microsoft/bitnet-b1.58-2B-4T` | ternary research runtime | BitNet runtime | watchlist | Runtime proof before benchmark claims | blocked |
| `mit-oasys/rlm-qwen3-8b-v0.1` | recursive research runtime | custom RLM harness | watchlist | Harness proof before Hermes claims | blocked |

## Current Recommendation

Do not keep scaling Qwen3 4B micro-tuning blindly. V4 is the current narrow
strict-tool-call winner; V5 showed that pilot polish can regress held-out
behavior. Run runtime and benchmark selection across better bases before broader
claims:

1. Keep Qwen3 v4 as the public/recommended local strict Hermes tool-call adapter.
2. Use LM Studio Qwen3, Hermes 4 14B, Qwen3.6 35B-A3B, and LFM2 24B-A2B as runtime baselines, not publication candidates.
3. Use BGE-M3 as the retrieval baseline while LFM2-ColBERT and Qwen retrieval candidates are triaged.
4. Keep research runtimes watchlisted until they can serve reproducible Hermes prompts.

## Synthesis

Current lane winners, no-publish decisions, and next parallel work are summarized in:

`reports/model-radar/candidate-selection-synthesis-20260524.md`
