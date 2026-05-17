# Future Model Candidates — Research Notes

Based on HuggingFace API research (2026-05-16).

## Near-Term (After Gemma 4 + LFM2 Complete)

| Model | Params | License | Downloads | Why |
|-------|--------|---------|-----------|-----|
| **Ministral 3 8B** | ~8B | Apache 2.0 | 151k | Edge-optimized, multilingual, clean license |
| **Qwen3 4B** | ~4B | Apache 2.0 | 9.3M | Fast on 32GB RAM, surprising quality |
| **Qwen2.5 7B** | ~7B | Apache 2.0 | 12.6M | Community standard LoRA target |
| **Llama 3.1 8B** | ~8B | Llama 3.1 | 10M | Broadest ecosystem support |

**Model size*: All under 10B params → fit in 32GB for LoRA training.

## Subquadratic / Long-Context Models (Experimental)

These use architectures that scale better than O(n²) attention:

| Model | Architecture | Context | Params | Sizes Available | Source | Status |
|-------|-------------|---------|--------|----------------|--------|--------|
| **RecurrentGemma** | Griffin (gated recurrences + local attention) | ~32K+ (linear) | 2B, 9B | ✅ HF GGUF | Google, Apache 2.0 | Most polished "recursive" model |
| **Mamba 2.8B** | SSM (state space model) | Linear in L | 130M–2.8B | ✅ HF | CMU/MIT, Apache 2.0 | Subquadratic, research-active |
| **Mamba2** | SSM v2 | Linear in L | 130M–2.8B | ✅ HF | CMU/MIT, Apache 2.0 | Improved training stability |
| **RWKV-6** | Linear RNN | Unlimited (practical) | 1.5B–14B | ✅ HF | Community | RNN-style, O(n) inference |
| **Hawk/Griffin** | Hybrid recurrent + attention | Linear in L | ~2B–9B | Research paper | Google DeepMind | Predecessor to RecurrentGemma |

**Reality check:** None of these offer a verified >10M context window in a production model today. They *scale subquadratically* (O(n) or O(n log n) instead of O(n²)), which means larger contexts are theoretically possible. Practically, most are trained with 8K–32K windows.

## Relevant Research Papers (MIT / CMU / Subquadratic)

| Paper | Year | Key Idea | Authors |
|-------|------|----------|--------|
| Mamba: Linear-Time Sequence Modeling | 2023 | Selective SSMs beat Transformers on long sequences | Gu & Dao |
| Mamba2: Transformers are SSMs | 2024 | Unified view, faster training | Gu & Dao |
| RecurrentGemma: Moving Past Transformers | 2024 | Griffin architecture at scale | Google DeepMind |
| Griffin: Hybrid Recurrent + Attention | 2024 | Gated linear recurrences + local attention | Google DeepMind |
| RWKV: Reinventing RNNs for Transformers | 2023 | Linear attention via time-mixing | RWKV community |

## What to Watch

As of mid-2026, the "MIT recursive models >10M context" the user mentioned may have been:
1. **Mamba/Mamba2** from Albert Gu (CMU → MIT) — the closest match to "MIT + subquadratic"
2. A pre-release announcement of a new model that hasn't hit HuggingFace yet
3. Research papers on "recursive composition" or "infinite context" that haven't been released as models
