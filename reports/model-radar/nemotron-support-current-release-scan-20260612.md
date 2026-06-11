# Nemotron Support Current Release Scan - 2026-06-12

## Summary

This scan records the newer Nemotron support models that matter for agent
deployment boundaries, moderation, and streaming speech.

## Verified Candidates

| Family | Verified release | Why it matters |
|---|---|---|
| NVIDIA | `nvidia/Nemotron-3.5-Content-Safety` | A multimodal/text safety moderator with explicit reasoning/custom-policy support. |
| NVIDIA | `nvidia/nemotron-3.5-asr-streaming-0.6b` | A low-latency streaming ASR model that is useful for speech-to-text plumbing and multimodal agent pipelines. |

## Packaging Note

- An MLX conversion exists for `nvidia/nemotron-3.5-asr-streaming-0.6b` as
  `mlx-community/nemotron-3.5-asr-streaming-0.6b`.

## Decision

- Add the Nemotron support models to the machine-readable radar.
- Keep them in specialist support lanes, not Hermes text-generation lanes.
- Do not claim runtime or promotion evidence from this scan alone.
