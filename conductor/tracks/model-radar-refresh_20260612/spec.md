# Specification: Model Radar Current Release Refresh

## Overview

The model radar needs a fresh pass so the repo reflects the newest verified
open-weight candidates that matter for Hermes-style local and cloud work.

This refresh focuses on:

- newer Hermes, Gemma, and Qwen releases that are actually published
- the current status of Qwen3.7 open weights
- candidate updates for 32GB Mac and Colab-assisted workflows

## Scope

- Verify current official/primary-source release status for the latest models.
- Update `MODEL_CANDIDATES.yaml` with newly verified candidates.
- Update `FUTURE_MODELS.md` and `HANDOFF.md` so the guidance matches the new
  radar.
- Record a short report summarizing what changed and what remains watchlist
  only.

## Out Of Scope

- No training runs.
- No runtime proof claims for the new candidates unless already proven in the
  repo.
- No publication or benchmark claims.

## Acceptance Criteria

- The radar reflects the newer open-weight releases relevant to Hermes work.
- Qwen3.7 remains watchlist-only until verified open weights exist.
- The docs stay consistent with the model-candidate table.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is source-backed, conservative, and only promotes
  models that are verified to exist.
- Remaining gap: runtime proof still has to happen separately for any new
  candidate.
