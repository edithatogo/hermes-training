# Specification: MiniCPM5 1B MLX Prompt Repair Completion

## Overview

The queued local prompt-only repair variants for `openbmb/MiniCPM5-1B-MLX` have
now been executed against the strict 3-case BFCL pilot. All three variants
scored `0/3` and remain no-promotion evidence only.

## Goals

- Record strict suffix, empty-output retry, and MiniCPM concise-tag repair
  outcomes.
- Keep SSD-backed source summaries linked from the result registry.
- Update the repair ledger so MiniCPM5 1B MLX is no longer pending local repair.
- Document the decision to stop prompt-only MiniCPM repairs.

## Acceptance Criteria

- Three MiniCPM repair reports are tracked under `reports/benchmark/local-pilots/`.
- The result registry records all three MiniCPM variants with
  `promotion_allowed: false`.
- The ledger records MiniCPM5 1B MLX as `completed-no-promotion`.
- Focused validators, Conductor consistency, and full readiness pass.

## Out Of Scope

- Promoting MiniCPM5 1B MLX.
- Launching cloud jobs.
- Implementing grammar/envelope-constrained generation.
