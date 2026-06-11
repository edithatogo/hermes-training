# Nemotron Frontier Current Release Scan - 2026-06-12

## Summary

This scan records the larger Nemotron frontier models that change the upper-end
comparison set for Hermes-style work.

## Verified Candidates

| Family | Verified release | Why it matters |
|---|---|---|
| NVIDIA | `nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16` | Multimodal Nano Omni reasoning model for enterprise Q&A, transcription, and document intelligence workflows. |
| NVIDIA | `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4` | Large general-purpose reasoning/chat model optimized for collaborative agents and long-context workloads. |
| NVIDIA | `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16` | Smaller reasoning/chat model with explicit reasoning-trace behavior. |
| NVIDIA | `nvidia/Qwen3-Nemotron-235B-A22B-GenRM-2603` | Reward model used in Nemotron training; useful as a teacher/evaluator reference, not a chat default. |

## Decision

- Add the verified Nemotron frontier entries to the machine-readable radar.
- Keep them in cloud-teacher or research-runtime lanes only.
- Do not claim runtime or promotion evidence from this scan alone.
