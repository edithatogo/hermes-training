# Specification: Nanbeige 4.1 3B Prompt Repair Completion

## Overview

The queued local repair variant for `Nanbeige/Nanbeige4.1-3B` has been executed
against the strict 3-case BFCL pilot. The model produced semantically correct
tool calls for the tool-call cases, but strict scoring failed because the output
included `<think>` traces and extra refusal explanation.

## Goals

- Record the strict-suffix repair outcome.
- Update the repair ledger so Nanbeige 4.1 3B is no longer pending local repair.
- Document that the remaining blocker is no-extra-text formatting, not argument
  selection.

## Acceptance Criteria

- The Nanbeige repair report is tracked under `reports/benchmark/local-pilots/`.
- The result registry records the variant with `promotion_allowed: false`.
- The ledger records Nanbeige 4.1 3B as `completed-no-promotion`.
- Focused validators, Conductor consistency, and full readiness pass.

## Out Of Scope

- Promoting Nanbeige 4.1 3B.
- Launching cloud jobs.
- Implementing no-think or grammar/envelope-constrained generation.
