# Live Hugging Face Refresh - 2026-06-13

## Scope

No-download live refresh for the bleeding-edge Hermes and mem0 roadmap.

Checked terms:

- `Qwen3.7`
- `Qwen3.6`
- `Gemma-4`
- `MiniCPM`
- `Nemotron-3`
- `LFM2.5`
- `LFM2-ColBERT`
- `Hermes-4`
- `bitnet-b1.58`
- `DeepSeek-V4`
- `MiniMax-M3`
- `Kimi-K2.6`
- `MiMo-V2.5`

The installed Hugging Face client rejected `sort=modified`; the supported
`sort=lastModified` path was used instead.

## Relevant Findings

| Finding | Evidence | Decision |
|---|---|---|
| MiniMax M3 surfaced as a fresh frontier lane. | `MiniMaxAI/MiniMax-M3`, `MiniMaxAI/MiniMax-M3-MXFP8`, `unsloth/MiniMax-M3`, and `unsloth/MiniMax-M3-GGUF` were modified on 2026-06-12 with multimodal/MoE/agent/coding tags. | Add as cloud/specialist runtime and GGUF packaging watchlist lanes; do not download until size/runtime support is known. |
| MiMo V2.5 remains relevant for specialist long-context work. | `XiaomiMiMo/MiMo-V2.5-Pro-FP4-DFlash`, AWQ packages, and MLX community packaging surfaced in the refresh. | Add one official/specialist lane; keep Mac-local work gated behind runtime and size proof. |
| Qwen3.7 still lacks a credible official open-weight lane. | Search found only `RscriptSQwen/Qwen3.7-plus`, with no official Qwen namespace hit. | Keep `qwen3.7-open-weights-watch` watchlist-only. |
| Qwen3.6, Gemma 4, MiniCPM, LFM2.5, BitNet, DeepSeek V4, Kimi K2.6, and Nemotron all have active packaging/fine-tune churn. | Latest hits were mostly community quants, LoRAs, or support packages already covered by the existing radar categories. | No automatic promotion. Runtime proof and strict benchmark evidence remain required. |

## Artificial Analysis Cross-Check

The Artificial Analysis small open-source page still presents Qwen3.6 27B and
Qwen3.6 35B A3B as the leading small open-source models. That supports keeping
the Qwen3.6 lanes high in the cloud/local proof queue, but it does not override
the local strict Hermes tool-call failures already recorded for the acquired
Qwen3.6 GGUF path.

## SSD Policy

No model files were downloaded for this refresh. All future acquisitions should
continue to run under `scripts/env.sh` so caches and benchmark outputs stay on
`/Volumes/PortableSSD`.
