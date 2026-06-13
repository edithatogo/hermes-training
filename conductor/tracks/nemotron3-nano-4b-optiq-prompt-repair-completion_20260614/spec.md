# Specification: Nemotron 3 Nano 4B OptiQ Prompt Repair Completion

## Overview

The queued local repair variant for
`mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` has been executed against
the strict 3-case BFCL pilot. It scored `0/3` and remains no-promotion evidence.

## Goals

- Record the strict-suffix repair outcome.
- Update the repair ledger so Nemotron 3 Nano 4B OptiQ is no longer pending
  local repair.
- Document the failure pattern for future constrained-output work.

## Acceptance Criteria

- The Nemotron repair report is tracked under `reports/benchmark/local-pilots/`.
- The result registry records the variant with `promotion_allowed: false`.
- The ledger records Nemotron 3 Nano 4B OptiQ as `completed-no-promotion`.
- Focused validators, Conductor consistency, and full readiness pass.

## Out Of Scope

- Promoting Nemotron 3 Nano 4B OptiQ.
- Launching cloud jobs.
- Implementing grammar/envelope-constrained generation.
