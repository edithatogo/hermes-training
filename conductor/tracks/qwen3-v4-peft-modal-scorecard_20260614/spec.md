# Specification: Qwen3 v4 PEFT Modal Scorecard

## Overview

Modal is authenticated locally and is a plausible custom-container fallback for
the no-limit Qwen3 v4 PEFT selected-task lm-eval scorecard. It must remain
fail-closed until free credit/grant status, GPU policy, result persistence, and
explicit run approval are all proven.

## Goals

- Add a Modal app script for the PEFT lm-eval selected scorecard.
- Add a guarded submitter that dry-runs by default.
- Stage the Modal scorecard config and dry-run report.
- Record result-persistence intent through a Modal volume plus local
  `--write-result` output.
- Keep remote execution blocked without both run and zero-cost confirmation.

## Acceptance Criteria

- The submitter emits a dry-run report without launching Modal work.
- Execution requires `--execute --confirm-modal-run --confirm-zero-cost-compute`.
- The command targets a T4 Modal function and writes returned output locally.
- The active blocked matrix maps this track to the `modal` backend.

## Out Of Scope

- Launching Modal GPU work.
- Treating empty current-month billing as credit/grant proof.
- Publishing Modal artifacts as benchmark evidence before recovery.
