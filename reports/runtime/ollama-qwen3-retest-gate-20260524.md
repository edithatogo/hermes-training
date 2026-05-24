# Ollama Qwen3 Retest Gate

Date: 2026-05-24

## Result

The Qwen3 GGUF/Ollama retest remains blocked.

Current local Ollama version:

```text
ollama version is 0.24.0
```

Current daemon state:

- Ollama is listening on `127.0.0.1:11434`.
- Already-installed models remain usable through the OpenAI-compatible endpoint.
- No evidence of an Ollama upgrade, rebuild, or installation change after the prior Qwen3 GGUF import/runtime failure was found in this pass.

## Decision

Do not rerun the Qwen3 GGUF import against this unchanged Ollama runtime. The prior failure mode was daemon instability during or after import, so repeating it without a runtime change would risk churn without adding evidence.

Use these validated alternatives for the same SSD-backed Qwen3 Q4_K_M artifact:

- llama.cpp: `reports/runtime/llamacpp-qwen3-q4km-server-smoke-20260524.md`
- LM Studio: `reports/runtime/lmstudio-qwen3-q4km-server-smoke-20260524.md`

## Reopen Gate

Reopen this retest only after one of these changes is true:

1. Ollama is upgraded or rebuilt after `0.24.0`.
2. The local Ollama repo lands a relevant Qwen3/GGUF/MLX runner fix.
3. A smaller importer-only smoke can validate the create path without risking the active daemon.
