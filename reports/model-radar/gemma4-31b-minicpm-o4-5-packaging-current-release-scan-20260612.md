# Gemma 4 31B and MiniCPM-o 4.5 Packaging Refresh - 2026-06-12

## Summary

This follow-up scan captures the latest explicit packaging lanes for Gemma 4
31B-it and MiniCPM-o 4.5 that are relevant to local Mac/LM Studio comparison
workflows.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| Gemma | `google/gemma-4-31B-it-qat-q4_0-gguf` | Official QAT q4_0 GGUF packaging lane for the Gemma 4 31B instruction model. |
| MiniCPM | `openbmb/MiniCPM-o-4_5-gguf` | Explicit GGUF packaging lane for the multimodal MiniCPM-o 4.5 model. |

## Watchlist Status

- Keep both lanes separate from new training claims.
- Runtime proof and helper workflow proof remain separate gates.

## Decision

- Add the new Gemma 4 31B QAT GGUF and MiniCPM-o 4.5 GGUF entries to
  `MODEL_CANDIDATES.yaml`.
- Update the radar docs so the packaging lanes are tracked separately from the
  base model cards.
