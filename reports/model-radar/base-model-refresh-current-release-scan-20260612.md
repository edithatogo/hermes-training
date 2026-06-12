# Base Model Release Follow-Up - 2026-06-12

## Summary

This follow-up scan captures the official base repos that were still missing from
the machine-readable candidate list after the main 2026-06-12 refresh.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| Gemma | `google/gemma-4-31B` | Official Gemma 4 31B base repo surfaced in the current Hugging Face collection; keep it as a teacher/comparison lane. |
| Qwen | `Qwen/Qwen3-Coder-Next` | Official base repo behind the subquadratic coding-agent lane; pair it with the GGUF runtime tree for Hermes-agent smoke. |
| MiniCPM | `openbmb/MiniCPM-V-4.6-GPTQ` | Fresh GPTQ packaging for the MiniCPM-V 4.6 multimodal lane; useful as a local packaging comparison point. |

## Watchlist Status

- `Qwen/Qwen3.7-*` still has no verified open-weight lane in the official search
  checked for this refresh.
- The base repos above are source-backed additions only; runtime proof remains a
  separate gate.

## Decision

- Add the new base-model repos to `MODEL_CANDIDATES.yaml`.
- Update the radar docs and handoff text to mention the follow-up refresh.
- Keep the existing local-runtime and teacher gating unchanged.
