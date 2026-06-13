# Specification: Constrained Envelope Repair Plan

## Overview

The local prompt/profile repair queue is exhausted: all Mac-local prompt-only
variants have completed without promotion. The next step is to identify whether
any candidate is worth a constrained-envelope or runtime-wrapper diagnostic,
while keeping promotion gates fail-closed.

## Scope

- Inspect the completed prompt/profile repair results and their SSD-backed
  per-case `results.jsonl` artifacts.
- Distinguish exact Hermes tool calls rejected only for extra text from malformed
  calls, empty outputs, and refusal-boundary failures.
- Rank candidates for the next constrained-envelope diagnostic.
- Add validation so the plan cannot claim promotion or drop strict
  `--require-no-extra-tool-text` scoring.

## Out Of Scope

- No model download.
- No model training.
- No endpoint launch.
- No cloud job.
- No adapter, model, or runtime promotion.

## Acceptance Criteria

- A JSON and Markdown constrained-envelope plan are generated under
  `reports/benchmark/coverage/`.
- Nanbeige 4.1 3B is identified as the top constrained-envelope candidate only
  because its completed local run produced exact Hermes calls with extra text.
- The plan includes non-promotional diagnostic commands that preserve strict
  no-extra-text scoring.
- Readiness validates the plan and fails if source evidence disappears.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.8 / 10`
- Evidence: the plan is derived from completed local benchmark artifacts and is
  enforced by unit tests plus full readiness validation.
- Remaining gap: actual constrained runtime-wrapper implementation and rerun
  evidence are separate tracks.
