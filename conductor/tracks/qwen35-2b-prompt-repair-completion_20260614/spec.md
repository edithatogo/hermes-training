# Specification: Qwen3.5 2B Prompt Repair Completion

## Overview

The queued local prompt-only repair variants for `Qwen/Qwen3.5-2B` have been
executed against the strict 3-case BFCL pilot. The no-think variant passed only
the invalid-tool refusal case; all variants failed exact Hermes tool-call
parsing and remain no-promotion evidence.

## Goals

- Record strict suffix, empty-output retry, and no-think prefill repair outcomes.
- Keep SSD-backed source summaries linked from the result registry.
- Update the repair ledger so Qwen3.5 2B is no longer pending local repair.
- Document the decision to stop prompt-only Qwen3.5 2B repairs.

## Acceptance Criteria

- Three Qwen3.5 2B repair reports are tracked under `reports/benchmark/local-pilots/`.
- The result registry records all three variants with `promotion_allowed: false`.
- The ledger records Qwen3.5 2B as `completed-no-promotion`.
- Focused validators, Conductor consistency, and full readiness pass.

## Out Of Scope

- Promoting Qwen3.5 2B.
- Launching cloud jobs.
- Implementing grammar/envelope-constrained generation.
