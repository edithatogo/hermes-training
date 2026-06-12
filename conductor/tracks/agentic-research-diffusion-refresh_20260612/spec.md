# Specification: Agentic Research and Diffusion Refresh

## Overview

The Hermes radar also needs to follow new agentic research models and the
latest diffusion-style text/VLM releases that matter for agent throughput and
research workflows.

This refresh focuses on:

- AgentCPM-Report as an 8B deep research agent
- MiniCPM-V 4.6 as a more capable multimodal helper
- Nemotron-Labs-Diffusion 14B and VLM 8B as speed/reasoning research lanes

## Scope

- Verify the current published status of the candidate repos.
- Add the verified candidates to `MODEL_CANDIDATES.yaml`.
- Update `FUTURE_MODELS.md` and `HANDOFF.md` with the new guidance.
- Record a concise scan report of the additions and guardrails.

## Out Of Scope

- No runtime proof claims for the new candidates.
- No training runs.
- No promotion of the new models to default local fine-tune targets.

## Acceptance Criteria

- The radar includes the new research and diffusion candidates.
- The docs make clear these are runtime or specialist-only lanes.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is source-backed and keeps the candidates in
  specialist/runtime lanes.
- Remaining gap: runtime proof is still separate for every candidate.
