# Emerging Frontier Current Release Scan

Date: 2026-06-12

This follow-up scan extends the existing frontier radar with newer multimodal
and teacher-scale open-weight releases. It does not claim runtime proof or
training readiness for any newly added model.

## What Changed

- `google/gemma-4-31B-it` is now tracked as the larger Gemma 4 teacher
  baseline, with a visible community GGUF packaging path for runtime
  comparison.
- `openbmb/MiniCPM-o-4_5` is now tracked as a multimodal helper/runtime lane,
  with official GGUF packaging and community MLX coverage visible.
- `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16` is now tracked as a
  frontier-scale NVIDIA teacher baseline.
- `deepseek-ai/DeepSeek-V4-Flash` is now tracked as a long-context cloud
  teacher/reference model.
- The BitNet/QVAC BitLoRA path is now called out as an emerging 1-bit
  fine-tuning support lane, but it is still a research/runtime path rather
  than a promotion target.

## Radar Summary

| Model | Status | Recommended lane |
|---|---|---|
| `google/gemma-4-31B-it` | Verified official open-weight repo | Cloud teacher / packaging comparison only |
| `openbmb/MiniCPM-o-4_5` | Verified official open-weight repo with GGUF/MLX packaging visible | Local helper/runtime lane for multimodal workflows |
| `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16` | Verified official frontier-scale repo | Cloud teacher only |
| `deepseek-ai/DeepSeek-V4-Flash` | Verified preview open-weight repo | Cloud teacher / long-context reference only |
| BitNet QVAC / BitLoRA | Verified ecosystem support article | Research/runtime support path only |

## Guardrails

- Keep `Qwen3.7` watchlist-only until official open weights appear.
- Do not treat the new teacher-scale models as local Mac fine-tune targets.
- Use the new multimodal model only if the workflow needs vision or audio,
  otherwise keep the existing Qwen3.6, Hermes 4.3, Gemma 4 12B, and
  MiniCPM5/BitNet lanes as the current local comparison set.

## Sources

- Google Gemma 4 model cards and collection pages
- OpenBMB MiniCPM-o 4.5 model cards and discussions
- NVIDIA Nemotron 3 Ultra model cards and collection pages
- DeepSeek-V4-Flash model card
- Hugging Face BitNet / QVAC BitLoRA fine-tuning article
