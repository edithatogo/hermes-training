# Specification: Gemma E4B Prompt Repair Completion

## Overview

The queued local repair variants for `mlx-community/gemma-4-E4B-it-qat-4bit`
have been executed against the strict 3-case BFCL pilot. Raw strict prompting
and the analysis-only Gemma native normalizer both scored `0/3`, so the
candidate remains no-promotion evidence.

## Goals

- Record the raw strict-suffix repair outcome.
- Record the Gemma native normalizer analysis outcome without promotion.
- Update the repair ledger so Gemma E4B is no longer pending local repair.
- Document that normalizer analysis did not clear strict scoring.

## Acceptance Criteria

- Two Gemma repair reports are tracked under `reports/benchmark/local-pilots/`.
- The result registry records both variants with `promotion_allowed: false`.
- The ledger records Gemma E4B as `completed-no-promotion`.
- Focused validators, Conductor consistency, and full readiness pass.

## Out Of Scope

- Promoting Gemma E4B from normalizer analysis.
- Launching cloud jobs.
- Implementing grammar/envelope-constrained generation.
