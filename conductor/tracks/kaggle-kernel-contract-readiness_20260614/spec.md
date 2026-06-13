# Specification: Kaggle Kernel Contract Readiness

## Overview

Kaggle is now the strongest prepared no-cost GPU route after authentication and
quota visibility were confirmed. Before any kernel push or run, the staged
kernel package should have a machine-checkable contract covering public inputs,
dry-run status, selected tasks, timeout bounds, output persistence, and the
operator approval boundary.

## Goals

- Validate the staged Kaggle kernel metadata and config.
- Validate the dry-run report still records no execution and no confirmation.
- Validate the preflight report shows Kaggle quota visibility.
- Produce JSON and Markdown contract reports.
- Add the contract validator to full readiness.

## Acceptance Criteria

- Contract status is `pass`.
- The report records no private data upload.
- The staged kernel uses the public PEFT adapter and public selected benchmark tasks.
- The runner writes outputs under `/kaggle/working`.
- Full readiness runs the Kaggle contract validator.

## Out Of Scope

- Pushing the Kaggle kernel.
- Running Kaggle GPU work.
- Changing benchmark tasks or model artifacts.
