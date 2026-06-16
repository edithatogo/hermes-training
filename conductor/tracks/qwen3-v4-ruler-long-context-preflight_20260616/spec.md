# Specification: Qwen3 v4 RULER Long-Context Preflight

## Overview

Prepare the RULER long-context official-candidate slice for the Qwen3 v4 Hermes
adapter. This track makes the first run stage concrete and records the current
runtime blocker without installing packages or running a long-context job.

## Goals

- Replace the queue's `<context>` placeholder with a concrete first-stage
  `max_seq_length` of 4096.
- Record a context ladder of 4096, 8192, and 16384 tokens for staged scaling.
- Verify the SSD-backed benchmark Python and RULER module availability.
- Add a dated preflight report that is explicit about whether the RULER slice
  can be launched now.
- Keep RULER coverage missing until scored artifacts exist.

## Acceptance Criteria

- Add `scripts/check_ruler_long_context_preflight.py`.
- Add `scripts/validate_ruler_long_context_preflight.py`.
- Generate the JSON and Markdown preflight reports under
  `reports/benchmark/official-candidates/`.
- Update the official-candidate queue command to use `--max_seq_length 4096`
  and a `ctx4096` output directory.
- Add focused unit tests.
- Wire validation into hub readiness.

## Out Of Scope

- Installing RULER.
- Running a long-context benchmark.
- Creating cloud resources.
- Claiming RULER or long-context performance.
