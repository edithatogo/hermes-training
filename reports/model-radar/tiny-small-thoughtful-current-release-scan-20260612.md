# Current Release Scan

Date: 2026-06-12

## Summary

This refresh adds the current dense Qwen3.5 mid-size teacher lane, a new
MiniCPM-V 4.6 Thinking helper path, and the new Nanbeige4.1-3B tiny-model
candidate.

The live scan found:

- `Qwen/Qwen3.5-27B` as an official dense Qwen3.5 model.
- `openbmb/MiniCPM-V-4.6-Thinking` and `openbmb/MiniCPM-V-4.6-Thinking-gguf`.
- `Nanbeige/Nanbeige4.1-3B` and `Mungert/Nanbeige4.1-3B-GGUF`.

The scan did not verify any official open-weight `Qwen3.7` lane.

## Relevant Findings

| Candidate | Evidence | Track Treatment |
|---|---|---|
| `Qwen/Qwen3.5-27B` | Official Hugging Face repo and community GGUF packaging surfaced in search. | Dense mid-size teacher / comparison bridge. |
| `openbmb/MiniCPM-V-4.6-Thinking` | Current Hugging Face search shows the Thinking variant and GGUF packaging. | Multimodal helper/runtime comparison point. |
| `Nanbeige/Nanbeige4.1-3B` | Current tiny-model leaderboard and official repo surfaced in search. | Tiny reasoning/helper candidate. |

## Guardrails

- No runtime proof is claimed for the new candidates.
- Qwen3.7 remains watchlist-only until official open weights appear.
- The new candidates stay in runtime or teacher lanes until proven.
