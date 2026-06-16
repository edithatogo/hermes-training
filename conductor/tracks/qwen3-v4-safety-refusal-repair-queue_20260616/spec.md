# Specification: Qwen3 v4 Safety/Refusal Repair Queue

## Overview

Turn the scored Qwen3 v4 safety/refusal failures into a compact repair queue
with explicit lanes, case IDs, target behavior, and acceptance gates. This track
does not modify model weights; it defines the next measurable repair work.

## Goals

- Separate the failure modes from the scored safety/refusal run:
  strict empty-think wrapper leakage and forbidden-name leakage in refusals.
- Preserve the baseline metrics from the scored run.
- Record the exact failing case IDs and forbidden markers.
- Set next-run gates that prevent publication until the pinned suite passes
  strictly and standardized safety suites are evaluated separately.
- Wire the queue into hub readiness so stale repair plans fail.

## Acceptance Criteria

- Add `scripts/build_safety_refusal_repair_queue.py`.
- Add `scripts/validate_safety_refusal_repair_queue.py`.
- Generate JSON and Markdown queue reports under
  `reports/benchmark/official-candidates/`.
- Add focused unit tests.
- Wire the validator into `scripts/validate_readiness.py`.
- Add this Conductor track to the registry.

## Out Of Scope

- Running another fine-tune.
- Changing the runtime normalizer.
- Claiming the safety/refusal benchmark is solved.
- Running standardized XSTest, SimpleSafetyTests, HarmBench, or other external
  safety suites.
