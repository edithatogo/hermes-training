# Specification: LFM2.5 Full-Smoke-Data Training and Evaluation

## Overview

Move from pipeline proof to a meaningful local training gate for `LiquidAI/LFM2.5-1.2B-Instruct` by training over the current checked-in dataset scale and evaluating base vs adapter.

## Requirements

- Use SSD-backed caches and temp files.
- Train beyond the 10-iteration smoke run using the current 219k-token train split.
- Preserve the smoke adapter as local-only artifact.
- Record dataset audit, config, trained tokens, loss, peak memory, and result.
- Run Hermes-local base vs adapter evaluation.

## Acceptance Criteria

- Training completes and saves an adapter.
- Run note exists under an ignored experiment directory and summary is promoted to docs.
- Evaluation outputs are stored under SSD-backed or ignored paths.
- No quality claims are made unless benchmark results support them.

## Out of Scope

- Full publishable candidate training.
- Hugging Face publication.
- Retrieval/embedding model training.
