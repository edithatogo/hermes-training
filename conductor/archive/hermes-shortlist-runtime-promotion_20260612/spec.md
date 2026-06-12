# Hermes Shortlist Runtime and Promotion Execution

## Overview

Execute the Hermes model shortlist crystallized in `FUTURE_MODELS.md`, `MODEL_CANDIDATES.yaml`, the completed model-radar scan report, and `HANDOFF.md`. The track turns the shortlist into repeatable promotion evidence across local Mac/Metal and offloaded cloud workflows, with Colab used first where it can reduce local load.

## Scope

- Run or update runtime proofs for the current Hermes shortlist:
  - `Qwen/Qwen3-4B-MLX-4bit`
  - `Qwen/Qwen3.5-0.8B`
  - `Qwen/Qwen3.5-2B`
  - `openbmb/MiniCPM5-1B` and compatible MLX/GGUF packaging
  - Hermes 4.3, Harmonic Hermes, Harmonic, and Qwen3.6 teacher/runtime comparison lanes where feasible
- Use Colab CLI as the preferred offload route for benchmark and smoke jobs that would otherwise overload the local Mac.
- Gate Azure and NVIDIA/NGC routes behind explicit login, quota, API-key, and cost/license preflights.
- Preserve strict local promotion evidence for any model proposed as a default Hermes runtime or fine-tuning base.
- Update benchmark scorecards, runtime proof queues, and candidate metadata after each execution slice.

## Out of Scope

- Public model publication without explicit approval.
- Paid cloud execution without quota/cost confirmation.
- Promotion of unsupported or unproven formats based only on leaderboard placement.
- Broad retraining beyond the model-specific smoke/pilot evidence needed for promotion decisions.

## Acceptance Criteria

- Every shortlist candidate has a current evidence state: promoted, retained for further proof, blocked, or rejected.
- Colab execution is attempted first for suitable benchmark/smoke tasks and produces reproducible commands or a documented blocker.
- Azure and NVIDIA/NGC are represented as gated execution backends with live preflight results before use.
- `FUTURE_MODELS.md`, `MODEL_CANDIDATES.yaml`, runtime proof queues, and benchmark reports agree on each candidate state.
- No model is promoted without strict benchmark, runtime, and format-normalization evidence.

## Health Target

This track should not be marked complete below health 9.5. The final state must be reproducible from repo instructions and must separate evidence-backed decisions from watchlist speculation.
