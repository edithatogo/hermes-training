# Current Release Scan

Date: 2026-06-12

## Summary

This refresh adds the new dense Qwen3.6 comparison point and tightens the
Gemma 4 packaging surface for the Hermes radar.

The live scan found:

- `Qwen/Qwen3.6-27B` as an official dense Qwen3.6 model.
- `Qwen/Qwen3.6-27B-FP8` as an official FP8 packaging variant.
- `unsloth/Qwen3.6-27B-GGUF` as a local GGUF packaging variant.
- `google/gemma-4-12B-it` and `google/gemma-4-12B` in the official Gemma 4
  collection.
- `unsloth/gemma-4-12b-it-GGUF` plus related Gemma 4 12B / 26B / 31B
  packaging in Unsloth.

The scan did not verify any official open-weight `Qwen3.7` lane.

## Relevant Findings

| Candidate | Evidence | Track Treatment |
|---|---|---|
| `Qwen/Qwen3.6-27B` | Official Hugging Face repo and current small-model leaderboard placement. | Dense frontier comparison point. |
| `Qwen/Qwen3.6-27B-FP8` | Official HF tree with local-app instructions. | Cloud-teacher / packaging comparison only. |
| `unsloth/Qwen3.6-27B-GGUF` | Official GGUF tree with llama.cpp / Hermes Agent instructions. | Local runtime comparison point. |
| `google/gemma-4-12B-it` / `google/gemma-4-12B` | Official Gemma 4 collection entries. | Mid-size runtime candidate. |
| `unsloth/gemma-4-12b-it-GGUF` | Recent Unsloth Gemma 4 GGUF packaging. | Local runtime comparison point. |

## Guardrails

- No runtime proof is claimed for the new candidates.
- Qwen3.7 remains watchlist-only until official open weights appear.
- The new candidates stay in runtime or teacher lanes until proven.
