# Gemma 4 31B Community GGUF Refresh - 2026-06-12

## Summary

This follow-up scan captures the fresh community GGUF packaging lane for
Gemma 4 31B-it published by bartowski.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| Gemma | `bartowski/google_gemma-4-31B-it-GGUF` | Fresh community GGUF packaging published today for the Gemma 4 31B instruction model. |

## Watchlist Status

- Keep this lane separate from the official QAT and LM Studio GGUF lanes.
- Runtime proof and helper workflow proof remain separate gates.

## Decision

- Add the fresh bartowski Gemma 4 31B GGUF packaging lane to `MODEL_CANDIDATES.yaml`.
- Update the radar docs so the community packaging lane is visible alongside
  the official QAT and LM Studio packs.
