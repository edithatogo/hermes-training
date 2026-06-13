# Official Source Model Radar Refresh - 2026-06-13

## Scope

This refresh cross-checks the June 13 live radar against official or primary
model sources before adding any new local training or benchmark tracks.

## Official Findings

| Candidate | Source evidence | Decision |
|---|---|---|
| Gemma 4 family | Google AI for Developers lists Gemma 4 in E2B, E4B, 12B, 31B, and 26B A4B sizes, with default precision and quantized paths. Google DeepMind also presents Gemma 4 benchmark results for 31B, 26B A4B, E4B, and E2B thinking variants. | Treat Gemma 4 as a confirmed open-model family. Promote E4B/QAT packages to Mac-local prompt/profile repair and keep 12B, 26B A4B, and 31B as runtime or teacher comparison lanes until strict Hermes tool-call proof exists. |
| Gemma 4 26B A4B | The Hugging Face model page describes a mixture-of-experts 26B A4B model where only a 4B subset is active during inference. | Keep as a high-priority local/cloud runtime candidate, not a local fine-tune default. It needs endpoint smoke, BFCL-style Hermes strict proof, and memory notes before promotion. |
| Gemma 4 no-thinking fine-tuning format | Google's Gemma 4 prompt-formatting documentation says no-thinking fine-tuning datasets for 26B A4B and 31B should include an empty thought channel. | Add this as a hard data-format requirement for any Gemma 4 Hermes fine-tune or adapter experiment. |
| Qwen3.6-27B | The official Qwen Hugging Face page describes Qwen3.6-27B as the first open-weight variant of Qwen3.6, compatible with common Transformers-style runtimes. | Keep as the verified dense Qwen3.6 comparison lane. It is a runtime/teacher candidate first; local fine-tune is still risky on 32GB. |
| Qwen3.7 | Current official Qwen organization search did not surface a verified Qwen3.7 open-weight repository. | Keep `qwen3.7-open-weights-watch` watchlist-only. Do not create runtime, fine-tune, or benchmark tracks from low-signal third-party names. |
| Qwen3-Coder-Next | Official Qwen Hugging Face search continues to surface Qwen3-Coder-Next activity. | Keep as a specialist coding-agent runtime lane, with GGUF/runtime proof before any Hermes claim. |

## Updated Execution Implications

- Do not train or benchmark Qwen3.7 locally until official open weights or a
  supported hosted API lane exists.
- Add Gemma 4 E4B and 26B A4B to the prompt/profile repair queue, but require a
  strict Hermes endpoint proof before treating either as a candidate default.
- Any Gemma 4 no-thinking dataset must preserve the empty thought channel format
  so the model is not taught a prompt format that conflicts with the official
  fine-tuning guidance.
- Qwen3.6-27B remains a useful dense comparison point for Hermes and mem0-adjacent
  tool workflows, but the current Qwen3 v4 PEFT benchmark completion still has
  higher priority than starting another adapter.

## Sources

- https://ai.google.dev/gemma/docs/core
- https://deepmind.google/models/gemma/gemma-4/
- https://huggingface.co/google/gemma-4-26B-A4B
- https://ai.google.dev/gemma/docs/core/prompt-formatting-gemma4
- https://huggingface.co/Qwen/Qwen3.6-27B
- https://huggingface.co/Qwen
