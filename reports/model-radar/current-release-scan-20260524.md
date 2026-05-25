# Current Release Scan

Date: 2026-05-24

## Summary

The scan found refreshed Qwen3.6, Gemma 4, Hermes 4, Unsloth, MiMo V2 Flash, LFM2, and RWKV runtime candidates. It did not find an official Qwen3.7 open-weight local model lane.

Live refresh during implementation also found no Hugging Face model results for `Qwen3.7` or `Qwen3.7-Max`. It did find API listings and news coverage for `Qwen3.7-Max`, but not open local weights. It also found additional downloadable Qwen3.6 IQ4_XS, MiMo V2 Flash, Hermes 4 14B, and LFM2 candidates, including LFM2-24B-A2B GGUF, ONNX, and MLX-bf16 variants. These should be treated as secondary runtime experiments after the primary Qwen3.6 Q4_K_M and Gemma 4 Q3_K_M proofs.

## Relevant Findings

| Candidate | Evidence | Track Treatment |
|---|---|---|
| `Qwen/Qwen3.6-27B` | Listed in current Hugging Face Qwen search results. | Runtime proof candidate. |
| `Qwen/Qwen3.6-35B-A3B` | Listed in current Hugging Face Qwen search results. | Frontier runtime/teacher candidate. |
| `unsloth/Qwen3.6-27B-UD-MLX-4bit` | Model card exposes MLX usage and Hermes Agent setup instructions. | Mac-local runtime proof candidate; size is still tight for 32GB. |
| `unsloth/Qwen3.6-27B-MTP-GGUF` and `unsloth/Qwen3.6-35B-A3B-MTP-GGUF` | Recent Unsloth GGUF listings. | LM Studio/Ollama runtime proof candidates. |
| `localweights/Qwen3.6-35B-A3B-MTP-IMAT-IQ4_XS-Q8nextn-GGUF` | Hugging Face API search result updated `2026-05-16`. | Secondary lower-memory Qwen3.6 runtime candidate after the canonical Q4_K_M proof. |
| `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF` | Hugging Face API search result updated `2026-05-07`. | Secondary lower-memory Qwen3.6 runtime candidate; review quant quality and license before use. |
| `google/gemma-4-26B-A4B-it` | Current official Gemma 4 listing. | Multimodal MoE runtime/teacher candidate. |
| `unsloth/gemma-4-26B-A4B-it-GGUF` | Recent Unsloth GGUF listing. | LM Studio/Ollama runtime proof candidate. |
| `nvidia/Gemma-4-26B-A4B-NVFP4` | Quantized Gemma 4 listing. | Cloud/specialist runtime candidate. |
| `NousResearch/Hermes-4-14B` | Current NousResearch listing. | Primary Hermes baseline/runtime target. |
| `NousResearch/Hermes-4.3-36B` and GGUF variants | Current NousResearch listings. | Newer Hermes baseline; likely cloud or quantized runtime target. |
| `SandLogicTechnologies/Hermes-4-14B-GGUF` and `mradermacher/Hermes-4-14B-GGUF` | Hugging Face model cards expose Q4/Q5 or broader GGUF variants. | Alternate Hermes 4 quant sources; the current local SandLogic Q4_K_M artifact is already runtime-proven. |
| `unsloth/MiMo-V2-Flash-GGUF` and `mradermacher/MiMo-V2-Flash-i1-GGUF` | Hugging Face API search found GGUF variants for the recursive/reasoning MiMo V2 Flash lane. | Research runtime proof candidate after Mac-local Qwen3.6/Gemma priorities. |
| `XiaomiMiMo/MiMo-V2-Flash` | Model card describes a 309B-total, 15B-active MoE with hybrid attention and multi-token prediction. | Too large for this Mac as a first local target; keep as Azure/specialist or heavily quantized GGUF research lane. |
| `LiquidAI/LFM2-8B-A1B-GGUF` | Hugging Face model card reports GGUF availability for an 8B-total, 1B-active LFM2 MoE-style candidate. | Stronger LFM-family runtime candidate than the 2.6B helper if the GGUF fits and serves locally. |
| `LiquidAI/LFM2-24B-A2B`, `LiquidAI/LFM2-24B-A2B-GGUF`, `LiquidAI/LFM2-24B-A2B-ONNX`, `LiquidAI/LFM2-24B-A2B-MLX-bf16`, and `NexaAI/LFM2-24B-A2B-GGUF` | Live Hugging Face API refresh found multiple official and community runtime packages. | High-priority LFM runtime experiment; not a first 32GB Mac fine-tune target until artifact-size and endpoint proofs pass. |
| `RWKV/RWKV7-Goose-World3-2.9B-HF` | Current RWKV listing. | Research runtime proof candidate. |

## Qwen3.7 Guardrail

No official `Qwen/Qwen3.7-*` open-weight model or official Qwen repository result was verified. Keep Qwen3.7 out of local runtime, training, Azure, GitHub, and Hugging Face publication lanes until an official model card or repository exists. Treat `Qwen3.7-Max` as API-only/watchlist for now, not as a Mac-local model.

## 2026-05-25 Refresh

Live Hugging Face search was refreshed on 2026-05-25 for `Qwen3.7`,
`Qwen3.6`, `Hermes-4.3`, `LFM2-24B-A2B`, `BitNet`, and `RWKV-7`.

- `Qwen3.7`: no Hugging Face model results were returned. Keep the guardrail.
- `Qwen3.6`: community GGUF/merged variants remain active; the local project
  already has the Qwen3.6 35B-A3B Q4_K_M runtime proof and should not add a
  second Qwen3.6 download unless it closes a specific benchmark gap.
- `Hermes-4.3`: newer 36B GGUF/MLX variants are visible, including MLX 5-bit
  and Q4/Q5 GGUF variants. This remains a cloud or carefully selected local
  runtime-proof candidate, not an M1 fine-tune target.
- `LFM2-24B-A2B`: additional terminal-SFT, MXFP4-MoE, OpenVINO int4, and GGUF
  variants are visible. The current LFM2-24B-A2B Q4 acquisition should finish
  and prove before adding another LFM2 variant.
- `BitNet`: small and experimental variants are visible, but no current result
  changes the existing watchlist-only posture.
- `RWKV-7`: `rwkv7-g1` and 7.2B/13.3B GGUF variants are visible. These remain
  research-runtime lanes until a Hermes prompt harness exists.

## Sources

- Hugging Face Qwen model search: `https://huggingface.co/models?search=Qwen%2FQwen3`
- Hugging Face Unsloth organization model search: `https://huggingface.co/unsloth/models`
- Hugging Face Gemma 4 model search: `https://huggingface.co/models?search=google%2Fgemma-4-26B-A4B`
- Hugging Face NousResearch organization: `https://huggingface.co/NousResearch`
- Hugging Face RWKV organization: `https://huggingface.co/RWKV/models`
- Live Hugging Face API searches on 2026-05-24 for `Qwen3.7`, `Qwen3.7-Max`, `Qwen3.6-35B-A3B`, `LFM2-24B-A2B`, `Hermes-4-14B`, and `MiMo-V2-Flash GGUF`
- Live Hugging Face API searches on 2026-05-25 for `Qwen3.7`, `Qwen3.6`, `Hermes-4.3`, `LFM2-24B-A2B`, `BitNet`, and `RWKV-7`
- Qwen3.7-Max web refresh: TechNode, GIGAZINE, VentureBeat, BenchLM, and related coverage describe a proprietary/API-preview model, not an open-weight local artifact.
- Hugging Face pages checked on 2026-05-24: `SandLogicTechnologies/Hermes-4-14B-GGUF`, `mradermacher/Hermes-4-14B-GGUF`, `XiaomiMiMo/MiMo-V2-Flash`, `LiquidAI/LFM2-8B-A1B-GGUF`, and Hugging Face model search results for `Qwen3.7`.
