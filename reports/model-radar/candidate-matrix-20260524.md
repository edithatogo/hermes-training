# Candidate Matrix

Date: 2026-05-24

This matrix turns the current model radar into execution decisions. It is not a benchmark result.

| Candidate | Lane | First Runtime | Decision State | Next Action | Publication State |
|---|---|---|---|---|---|
| `Qwen/Qwen3-4B-MLX-4bit` v6 free-text-copy LoRA iter125 | Mac-local fine-tune | MLX local generation/server | current local strict Hermes tool-call adapter candidate | Use `gemma4/experiments/qwen3-4b-strict-toolcall-v6-free-text-copy/lora_adapter_iter125`; package only after publication bundle refresh | local candidate, publication refresh pending |
| `Qwen/Qwen3-4B-MLX-4bit` v4 targeted LoRA | Mac-local fine-tune | MLX local generation/server | publishable narrow adapter candidate | Keep v4 as current strict Hermes tool-call adapter; broader claims need official benchmarks | public adapter approved, dataset separate |
| `LiquidAI/LFM2.5-8B-A1B` | Mac-local runtime/teacher | llama.cpp GGUF | runtime-proof only | Runtime load and bounded generation passed from SSD-backed Q4_K_M GGUF, but JSON compliance failed; keep as LFM runtime baseline only | runtime-only |
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
| `google/gemma-4-E4B-it-qat-q4_0-gguf` / `mlx-community/gemma-4-E4B-it-qat-4bit` | Mac-local runtime | MLX / llama.cpp | runtime-proof only | MLX load/scoring passed, but BFCL-style pilot stayed at `0.000`; keep for prompt/profile experiments, not strict Hermes promotion | runtime-only |
| `google/gemma-4-E2B-it-qat-q4_0-gguf` | Mac-local runtime | llama.cpp / LM Studio / Ollama | runtime-proof only | Official QAT q4_0 GGUF load passed, but bounded output was end-of-text only; retry only with a model-specific chat profile | runtime-only |
| `google/gemma-4-12B-it-qat-q4_0-gguf` | Mac-local runtime | llama.cpp / LM Studio / Ollama | priority runtime-proof candidate | Smoke after E4B; better quality target before 26B A4B/31B | blocked |
| `google/gemma-4-26B-A4B-it-qat-q4_0-gguf` | Mac-local runtime | llama.cpp / LM Studio / Ollama | priority runtime-proof candidate | QAT Q4_0 GGUF should be smoked before generic Gemma 4 GGUF variants | blocked |
| `google/gemma-4-31B-it-qat-q4_0-gguf` | Mac-local or Azure runtime | llama.cpp / LM Studio / Azure | secondary runtime-proof candidate | Artificial Analysis ranks 31B highly, but on 32GB Mac this follows E4B/12B/26B proof | blocked |
| `unsloth/gemma-4-26B-A4B-it-qat-GGUF` | Mac-local runtime | llama.cpp / LM Studio / Ollama | runtime-proof candidate | Alternate QAT GGUF packaging; validate only if Google QAT path is blocked or lower quality | blocked |
| `unsloth/gemma-4-26B-A4B-it-GGUF` | Mac-local runtime | LM Studio / Ollama | secondary runtime-proof candidate | Keep behind QAT packaging unless a specific runtime requires this package | blocked |
| `nvidia/Gemma-4-26B-A4B-NVFP4` | specialist/cloud runtime | NVIDIA stack | research-runtime candidate | Azure/specialist proof only | blocked |
| `LiquidAI/LFM2-ColBERT-350M` | retrieval | PyLate / sentence-transformers | retrieval candidate | Add retrieval smoke/MTEB-style lane | no chat adapter publication |
| `Qwen/Qwen3-Embedding-4B` | retrieval | sentence-transformers / Transformers | retrieval candidate | Batch/memory smoke before claims | no chat adapter publication |
| `Qwen/Qwen3-Reranker-4B` | retrieval | Transformers reranker | retrieval candidate | Reranker smoke after embedding baseline | no chat adapter publication |
| `BAAI/bge-m3` | retrieval baseline | FlagEmbedding / sentence-transformers | ready baseline | Use as practical retrieval baseline | no chat adapter publication |
| `LiquidAI/LFM2-24B-A2B-GGUF` | efficient LFM runtime | llama.cpp GGUF | runtime-proven baseline | Use as LFM comparison lane; strict held-out score is `0.375` and IFEval/coding pilots are `1.000` | runtime-only |
| `LiquidAI/LFM2-8B-A1B-GGUF` | efficient LFM runtime | llama.cpp / LM Studio | watchlist | Consider only if a smaller LFM runtime is needed after 24B evidence | blocked |
| `openbmb/MiniCPM5-1B` | tiny local runtime | MLX / GGUF / Transformers | helper-runtime only | MLX runtime and 100-prompt helper pass completed quickly, but strict BFCL-style tool-call pilot scored `0.000` | helper-only |
| `openbmb/MiniCPM5-1B-GGUF` / `openbmb/MiniCPM5-1B-MLX` | tiny local runtime | llama.cpp / MLX | helper-runtime only | Prefer MLX for fast helper/extraction experiments; do not treat as Hermes strict tool-call replacement | helper-only |
| `microsoft/bitnet-b1.58-2B-4T-gguf` | 1-bit efficiency runtime | BitNet specialist path | runtime-proof only | Native BitNet load and generation passed from SSD artifacts, but JSON instruction compliance failed | runtime-only |
| `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4` | NVIDIA/cloud baseline | NVIDIA stack / Azure | cloud/specialist runtime candidate | Strong small-board candidate, but NVFP4 is not a Mac-first runtime | blocked |
| `nvidia/NVIDIA-Nemotron-Nano-9B-v2` | NVIDIA/cloud/local GGUF fallback | NVIDIA stack / community GGUF / MLX community | runtime-watch candidate | Smaller NVIDIA lane; local proof only if GGUF/MLX packaging beats Gemma/LFM priorities | blocked |
| `nvidia/NVIDIA-Nemotron-Nano-12B-v2-VL-BF16` | multimodal cloud baseline | NVIDIA stack / community GGUF | cloud/specialist multimodal candidate | Track for GUI/screenshot agent comparisons after Qwen3-VL proof | blocked |
| `XiaomiMiMo/MiMo-V2-Flash` | large MoE research runtime | KTransformers / specialist GGUF / Azure | watchlist | Do not download locally first; test via Azure/specialist quant only after Qwen3.6 and Gemma queues clear | blocked |
| `Qwen/Qwen3-Coder-Next` | coding-agent baseline | SGLang / vLLM / Docker Model Runner / GGUF quant | cloud/specialist runtime candidate | Add Azure or specialist runtime smoke; not a 32GB Mac fine-tune target | blocked |
| `Qwen/Qwen3-VL-8B-Instruct-GGUF` | multimodal Hermes-agent runtime | llama.cpp / LM Studio / Ollama | multimodal runtime candidate | Smoke after text/tool-call and mem0 lanes if GUI/screenshot agent work becomes priority | blocked |
| `RWKV/RWKV7-Goose-World3-2.9B-HF` | recurrent research runtime | Transformers / specialist runtime | watchlist | Add after runtime harness proof | blocked |
| `microsoft/bitnet-b1.58-2B-4T` | ternary research runtime | BitNet runtime | runtime-proof only | Runtime proof exists through native BitNet; Hermes prompt/profile compliance remains the blocker | runtime-only |
| `mit-oasys/rlm-qwen3-8b-v0.1` | recursive research runtime | custom RLM harness | watchlist | Harness proof before Hermes claims | blocked |

## Current Recommendation

Do not keep scaling Qwen3 4B micro-tuning blindly. As of the 2026-06-13 v6
checkpoint comparison, v6 iter125 is the current local strict-tool-call winner:
it passes held-out and mirrored strict suites at `1.000`. V4 remains the last
publication-bundled adapter until the v6 bundle is refreshed, and V5/final170
show that pilot polish or extra training can regress held-out behavior. Run
runtime and benchmark selection across better bases before broader claims:

1. Use Qwen3 v6 iter125 as the local Hermes strict tool-call adapter candidate;
   keep Qwen3 v4 as the previous publication-bundled adapter until v6 packaging
   is complete.
2. Next local runtime proofs should prioritize Gemma 4 12B/26B QAT and Hermes 4.3 only after deciding the SSD/time cost is justified; LFM2.5-8B, Gemma E2B/E4B, MiniCPM5, and BitNet now have runtime-only evidence.
3. Use Gemma 4 26B A4B/31B QAT, Hermes 4 14B, Qwen3.6 35B-A3B, and LFM2 24B-A2B as larger comparison baselines, not publication candidates.
4. Use BGE-M3 as the retrieval baseline while LFM2-ColBERT and Qwen retrieval candidates are triaged.
5. Keep Qwen3-Coder-Next, NVIDIA Nemotron, RWKV, Mamba, MiMo, and Qwen3-VL watchlisted until they can serve reproducible Hermes prompts; BitNet is runtime-proven but still prompt/profile-blocked.

## Synthesis

Current lane winners, no-publish decisions, and next parallel work are summarized in:

`reports/model-radar/candidate-selection-synthesis-20260524.md`
