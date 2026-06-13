# Specification: Granite 4.1 3B Prompt Repair Completion

## Overview

The queued local repair variants for `ibm-granite/granite-4.1-3b` have been
executed against the strict 3-case BFCL pilot. Raw strict prompting and the
analysis-only Granite native normalizer both scored `1/3`, passing only the
invalid-tool refusal case.

## Goals

- Record the raw strict-suffix repair outcome.
- Record the Granite native normalizer analysis outcome without promotion.
- Update the repair ledger so Granite 4.1 3B is no longer pending local repair.
- Document that exact Hermes tool-call parsing remains failed.

## Acceptance Criteria

- Two Granite repair reports are tracked under `reports/benchmark/local-pilots/`.
- The result registry records both variants with `promotion_allowed: false`.
- The ledger records Granite 4.1 3B as `completed-no-promotion`.
- Focused validators, Conductor consistency, and full readiness pass.

## Out Of Scope

- Promoting Granite 4.1 3B from normalizer analysis.
- Launching cloud jobs.
- Implementing grammar/envelope-constrained generation.
