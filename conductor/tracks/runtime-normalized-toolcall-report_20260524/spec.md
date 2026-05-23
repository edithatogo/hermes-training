# Specification: Runtime-Normalized Tool-Call Report

## Overview

Create a first-class report for Hermes runtime-normalized tool-call behavior using the existing strict benchmark scorecard. This separates integration recoverability from publication quality.

## Requirements

- Preserve strict benchmark scoring and the `1.000` held-out publication gate.
- Summarize strict pass rate and runtime-normalized pass rate from existing `results.jsonl` files.
- Record rescued case IDs and residual runtime failures.
- Write generated report artifacts to SSD-backed evaluation storage.
- Update documentation so runtime normalization is explicit integration evidence only.

## Acceptance Criteria

- `scripts/summarize_runtime_normalized_tool_calls.py` exists.
- The script compiles and writes `summary.json` plus `summary.md`.
- A runtime report is generated from the V3 held-out Qwen3 scorecard under `/Volumes/PortableSSD/hermes-evals/`.
- Project docs point to the generated report and keep Hugging Face publication blocked.
