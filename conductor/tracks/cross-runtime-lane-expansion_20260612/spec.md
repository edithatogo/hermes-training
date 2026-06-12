# Specification: Cross Runtime Lane Expansion

## Overview

Hermes work needs a clear runtime matrix so model selection is not tied to a
single serving tool or one Mac-only path.

This track formalizes support for:

- `llama.cpp`
- Ollama
- LM Studio
- MLX / Metal-specific local paths
- external scale-out lanes such as Colab, Azure, Kaggle, and NVIDIA tooling

## Scope

- Record the practical runtime lanes already in use or under consideration.
- Tie newly surfaced packaging artifacts to the correct runtime lane.
- Keep Mac-local, cloud-scale, and hosted-tooling lanes separate in the docs.
- Preserve the current no-secret, no-public-push boundary for external accounts.

## Out Of Scope

- No cloud spending without preflight or quota checks.
- No credential setup or account changes in this slice.
- No training runs.

## Acceptance Criteria

- The runtime matrix is explicit in the candidate radar and handoff docs.
- The repo notes the practical difference between local Mac serving and
  external execution lanes.
- Metal-specific and packaging-specific guidance is visible where relevant.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the runtime matrix is documentation-first and bounded by existing
  tooling.
- Remaining gap: each runtime lane still needs its own proof run.
