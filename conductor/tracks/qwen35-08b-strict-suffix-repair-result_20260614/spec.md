# Specification: Qwen3.5 0.8B Strict-Suffix Repair Result

## Overview

The first prompt/profile repair run for `Qwen/Qwen3.5-0.8B` completed locally.
It used the `strict-suffix-copy-exact` variant and failed all strict BFCL pilot
cases. The run also exposed that generated experiment commands quoted the
`$(date ...)` expression inside `--run-id`, creating a literal output directory.

## Goals

- Record the completed repair result as no-promotion evidence.
- Update the execution ledger from pending to completed-no-promotion.
- Fix generated experiment command templates to use expandable `RUN_STAMP`.
- Validate the result registry and report.

## Acceptance Criteria

- The Qwen3.5 0.8B strict-suffix repair report is tracked.
- The result registry records `pass_rate: 0.0`, `cases: 3`, and `passed: 0`.
- The ledger records the candidate as `completed-no-promotion`.
- Generated experiment commands no longer place a literal `$(date ...)` inside
  `--run-id`.
- Focused tests, result/ledger validators, Conductor consistency, and full
  readiness pass.

## Out Of Scope

- Rerunning the same repair experiment.
- Promoting Qwen3.5 0.8B.
- Running the remaining repair variants.
