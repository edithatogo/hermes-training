# NVIDIA Nemotron Follow-Up - 2026-06-12

## Summary

This follow-up scan captures official NVIDIA repos that matter for Hermes-adjacent
work but were not yet explicit in the machine-readable candidate list.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| NVIDIA | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-Base-BF16` | Official base checkpoint for the Nemotron 3 Ultra family; useful for teacher/comparison work. |
| NVIDIA | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-GenRM` | Official generative reward model for the Nemotron 3 Ultra family; useful for evaluator/reward-lane comparisons. |
| NVIDIA | `nvidia/nemotron-speech-streaming-en-0.6b` | English streaming ASR checkpoint surfaced alongside the multilingual 3.5 release; useful as a speech support lane. |

## Watchlist Status

- `Qwen/Qwen3.7-*` still has no verified open-weight lane in the official search
  checked for this refresh.
- These NVIDIA additions are source-backed only; runtime proof remains a separate gate.

## Decision

- Add the new NVIDIA repos to `MODEL_CANDIDATES.yaml`.
- Update the radar docs and handoff text to mention the follow-up refresh.
- Keep the existing local-runtime and teacher gating unchanged.
