# Specification: Specialist Frontier Agentic Refresh

## Overview

The Hermes radar also needs to track newly published agentic teacher models and
specialist-runtime releases that are useful for comparison, distillation, or
future runtime experiments.

This refresh focuses on:

- Cohere Command A+ as a large agentic teacher
- StepFun Step 3.7 Flash as a large agentic and reasoning-heavy teacher
- Nex-N2-mini as a smaller agentic candidate with a local MLX conversion path

## Scope

- Verify the current published status of the specialist frontier candidates.
- Add the verified candidates to `MODEL_CANDIDATES.yaml`.
- Update `FUTURE_MODELS.md` and `HANDOFF.md` with the new agentic frontier
  guidance.
- Record a concise report of the additions and guardrails.

## Out Of Scope

- No runtime proof claims for the new candidates.
- No training runs.
- No promotion of the specialist models to default local fine-tune targets.

## Acceptance Criteria

- The radar includes the new specialist frontier candidates.
- The docs make clear these are teacher/runtime or specialist-only lanes.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.5 / 10`
- Evidence: the refresh is source-backed and does not overclaim local
  fit.
- Remaining gap: runtime proof is still separate for every candidate.
