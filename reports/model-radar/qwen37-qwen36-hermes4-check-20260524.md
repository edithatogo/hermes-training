# Frontier Model Availability Check

Date: 2026-05-24

## Findings

| Model | Status | Action |
|---|---|---|
| `Qwen/Qwen3.6-35B-A3B` | Verified on Hugging Face; updated `2026-04-24`; 35B total / 3B active; 26 safetensor shards | Keep as priority frontier runtime target and cloud teacher candidate. |
| `NousResearch/Hermes-4-14B` | Verified on Hugging Face; updated `2026-01-09`; safetensors available | Keep as primary Hermes baseline/teacher. |
| `unsloth/Qwen3.6-35B-A3B` | Verified on Hugging Face; updated `2026-05-11` | Track as an Unsloth-packaged training/runtime path, license review required. |
| `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX` | Verified on Hugging Face; MLX artifact path, updated `2026-04-17` | Candidate Mac runtime artifact if explicit download is approved. |
| `deepsweet/Qwen3.6-35B-A3B-MLX-oQ4` | Verified on Hugging Face; updated `2026-05-10` | Candidate Mac runtime artifact if explicit download is approved. |
| `mlx-community/Qwen3.6-35B-A3B-bf16` | Verified on Hugging Face; updated `2026-04-16` | Likely too large for 32GB local runtime unless quantized; cloud/transformers path first. |
| Qwen3.7 / Qwen3.7-Max | Current reports describe API/preview/proprietary availability; no official open-weight Hugging Face repo was verified | Do not create a local fine-tune/runtime track yet. Watch for official `Qwen/*Qwen3.7*` weights or supported hosted API workflow. |

## 2026-05-24 Refresh

Additional live checks found no Hugging Face API results for `Qwen3.7` or `Qwen3.7-Max`. Web results published between 2026-05-20 and 2026-05-24 describe Qwen3.7-Max as a proprietary/preview agent model, not an open-weight local artifact. The local work should therefore continue on Qwen3.6, Hermes 4, Gemma 4, MiMo, RWKV, BitNet, and LFM lanes until an official open-weight Qwen3.7 repository exists.

The refresh did identify secondary Qwen3.6 IQ4_XS GGUF candidates and MiMo V2 Flash GGUF candidates, but these are lower-priority experiments behind the canonical Qwen3.6 Q4_K_M and Gemma 4 Q3_K_M runtime proofs.

## Sources

- [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B)
- [NousResearch/Hermes-4-14B](https://huggingface.co/NousResearch/Hermes-4-14B)
- [Unsloth Qwen3.6 fine-tunes list](https://huggingface.co/models?other=base_model%3Afinetune%3AQwen%2FQwen3.6-35B-A3B)
- [Qwen3.7-Max coverage, closed/proprietary status](https://venturebeat.com/technology/alibabas-proprietary-qwen3-7-max-can-run-for-35-hours-autonomously-and-supports-external-harnesses-like-anthropics-claude-code)
- [Qwen3.7-Max TechNode coverage](https://technode.com/2026/05/21/alibaba-introduces-qwen3-7-max-as-next-gen-ai-agent-model/)
- [Qwen3.7-Max BenchLM listing](https://benchlm.ai/models/qwen3-7-max)
- [Qwen 3.7 local availability note](https://codersera.com/blog/how-to-run-qwen-3-7-locally-2026/)

## Decision

Qwen3.6 and Hermes 4 are real acquisition/runtime-proof targets. Qwen3.7 should remain watchlist-only until open weights or a supported hosted API path are available.
