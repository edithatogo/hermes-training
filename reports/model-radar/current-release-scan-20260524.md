# Current Release Scan

Date: 2026-05-24

## Summary

The scan found refreshed Qwen3.6, Gemma 4, Hermes 4, Unsloth, and RWKV runtime candidates. It did not find an official Qwen3.7 open-weight local model lane.

## Relevant Findings

| Candidate | Evidence | Track Treatment |
|---|---|---|
| `Qwen/Qwen3.6-27B` | Listed in current Hugging Face Qwen search results. | Runtime proof candidate. |
| `Qwen/Qwen3.6-35B-A3B` | Listed in current Hugging Face Qwen search results. | Frontier runtime/teacher candidate. |
| `unsloth/Qwen3.6-27B-UD-MLX-4bit` | Model card exposes MLX usage and Hermes Agent setup instructions. | Mac-local runtime proof candidate; size is still tight for 32GB. |
| `unsloth/Qwen3.6-27B-MTP-GGUF` and `unsloth/Qwen3.6-35B-A3B-MTP-GGUF` | Recent Unsloth GGUF listings. | LM Studio/Ollama runtime proof candidates. |
| `google/gemma-4-26B-A4B-it` | Current official Gemma 4 listing. | Multimodal MoE runtime/teacher candidate. |
| `unsloth/gemma-4-26B-A4B-it-GGUF` | Recent Unsloth GGUF listing. | LM Studio/Ollama runtime proof candidate. |
| `nvidia/Gemma-4-26B-A4B-NVFP4` | Quantized Gemma 4 listing. | Cloud/specialist runtime candidate. |
| `NousResearch/Hermes-4-14B` | Current NousResearch listing. | Primary Hermes baseline/runtime target. |
| `NousResearch/Hermes-4.3-36B` and GGUF variants | Current NousResearch listings. | Newer Hermes baseline; likely cloud or quantized runtime target. |
| `RWKV/RWKV7-Goose-World3-2.9B-HF` | Current RWKV listing. | Research runtime proof candidate. |

## Qwen3.7 Guardrail

No official `Qwen/Qwen3.7-*` open-weight model or official Qwen repository result was verified. Keep Qwen3.7 out of local runtime, training, Azure, GitHub, and Hugging Face publication lanes until an official model card or repository exists.

## Sources

- Hugging Face Qwen model search: `https://huggingface.co/models?search=Qwen%2FQwen3`
- Hugging Face Unsloth organization model search: `https://huggingface.co/unsloth/models`
- Hugging Face Gemma 4 model search: `https://huggingface.co/models?search=google%2Fgemma-4-26B-A4B`
- Hugging Face NousResearch organization: `https://huggingface.co/NousResearch`
- Hugging Face RWKV organization: `https://huggingface.co/RWKV/models`
