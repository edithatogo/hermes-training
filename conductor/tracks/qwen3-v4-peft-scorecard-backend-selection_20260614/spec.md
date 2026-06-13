# Specification: Qwen3 v4 PEFT Scorecard Backend Selection

## Overview

The Qwen3 v4 PEFT no-limit scorecard has multiple prepared execution lanes, but
the next action should not be inferred manually from scattered blocked tracks.
This track adds a deterministic selector that ranks the available backends from
the existing cloud unblock checklist while preserving remote-execution gates.

## Scope

- Read `reports/cloud/backend-unblock-checklist-20260613.json`.
- Produce compact JSON and Markdown selection reports under `reports/cloud/`.
- Rank backends by readiness while penalizing Colab no-limit retries while
  keepalive/session-pruning blockers remain.
- Keep the selected route non-executable until explicit approval, cost or
  zero-cost policy confirmation, and artifact recovery gates are satisfied.
- Validate the generated report in readiness.

## Out Of Scope

- No cloud login.
- No Kaggle kernel push.
- No paid or remote job submission.
- No benchmark promotion.
- No result-artifact claim.

## Decision

Kaggle is the next prepared backend for the Qwen3 v4 PEFT no-limit scorecard,
but only after explicit run approval. Colab should not be retried for no-limit
scorecard shards until the keepalive/session-pruning blocker is fixed.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: the selector is generated from tracked checklist state, covered by
  unit tests, and validated by readiness.
- Remaining gap: the actual no-limit benchmark still needs an approved backend
  execution and recovered SSD artifacts.
