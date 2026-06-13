# Specification: Qwen3.5 0.8B Prompt Repair Completion

## Overview

The remaining local prompt-only repair variants for `Qwen/Qwen3.5-0.8B` have
now been executed against the strict 3-case BFCL pilot. The `qwen-no-think-prefill`
variant improved refusal behavior but still failed exact Hermes tool-call
parsing. The `empty-output-retry` variant did not improve the strict pass rate.

## Goals

- Record the no-think and empty-output retry repair outcomes as no-promotion
  evidence.
- Keep all source summaries under the SSD-backed evaluation root.
- Update the result registry and ledger so the candidate shows completed repair
  variants without implying promotion.
- Document the next decision: stop prompt-only Qwen3.5 0.8B repairs and use a
  grammar/envelope-constrained path or move to the next queued candidate.

## Acceptance Criteria

- The no-think and empty-output retry reports are tracked under
  `reports/benchmark/local-pilots/`.
- The result registry records all three prompt-only variants with
  `promotion_allowed: false`.
- The ledger records completed variants and report paths for Qwen3.5 0.8B while
  keeping the best observed strict pass rate visible.
- Handoff notes state that Qwen3.5 0.8B prompt-only repair is exhausted.
- Focused tests, prompt/profile validators, Conductor consistency, and full
  readiness pass.

## Out Of Scope

- Promoting Qwen3.5 0.8B.
- Launching cloud jobs.
- Implementing the grammar/envelope-constrained runtime path.
