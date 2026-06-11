# Specification: Nemotron Frontier Model Refresh

## Overview

The specialist frontier needs a separate record for the larger Nemotron v3
models that matter as cloud teachers, reward models, or high-end runtime
comparisons.

This refresh focuses on:

- Nemotron 3 Nano Omni reasoning
- Nemotron 3 Super NVFP4
- Qwen3-Nemotron reward modeling

## Scope

- Verify the current published status of the larger Nemotron frontier models.
- Add the verified candidate entries to `MODEL_CANDIDATES.yaml`.
- Update `FUTURE_MODELS.md` and `HANDOFF.md` with the frontier guidance.
- Record a concise report of the additions and guardrails.

## Out Of Scope

- No runtime proof claims for the new models.
- No training runs.
- No promotion to local Mac fine-tune defaults.

## Acceptance Criteria

- The radar includes the larger Nemotron frontier entries.
- The docs make clear these are cloud-teacher or research-runtime candidates.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.5 / 10`
- Evidence: the refresh is source-backed and records the true upper-end
  comparison set.
- Remaining gap: runtime proof is still separate for each candidate.
