# Specification: Benchmark and Publication Hardening

## Overview

Create a benchmark and documentation system strong enough to support GitHub and Hugging Face publication without overstating smoke-run results.

## Requirements

- Maintain a Hermes-local benchmark plan.
- Maintain a standard benchmark matrix for comparable claims.
- Maintain a documentation and model-card publication plan.
- Keep benchmark caches and outputs on the SSD.
- Add scripts or commands that make dataset/token audits repeatable.

## Acceptance Criteria

- `BENCHMARKING_PLAN.md`, `STANDARD_BENCHMARKS.md`, and `DOCUMENTATION_PLAN.md` exist.
- `scripts/env.sh` exports SSD-backed benchmark/cache paths.
- `scripts/dataset_token_audit.py` runs against LFM2.5 splits.
- `scripts/validate_readiness.py` passes.

## Out of Scope

- Running the full benchmark suite.
- Publishing to Hugging Face.
- Claiming quality improvements from smoke adapters.
