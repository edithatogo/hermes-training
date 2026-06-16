# Plan: Qwen3 v4 Safety/Refusal Repair Queue

## Phase 1 - Failure Classification

- [x] Task: inspect the scored safety/refusal result.
- [x] Task: classify the empty-think wrapper failures.
- [x] Task: classify the forbidden-name refusal failures.

## Phase 2 - Queue Generation

- [x] Task: add `scripts/build_safety_refusal_repair_queue.py`.
- [x] Task: include baseline metrics and target next-run gates.
- [x] Task: include exact case IDs and forbidden markers.
- [x] Task: generate JSON and Markdown reports.

## Phase 3 - Validation And Readiness

- [x] Task: add `scripts/validate_safety_refusal_repair_queue.py`.
- [x] Task: add focused unit tests.
- [x] Task: wire the queue validator into `scripts/validate_readiness.py`.
- [x] Task: add this Conductor track to the registry.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: repair lanes are generated from scored evidence, the queue is
  validator-backed, focused tests pass, and the full readiness suite includes
  the new validator.
- Remaining gap: this is a planning artifact. The model still needs a repair
  run or runtime-profile experiment, followed by a strict rerun.
- Decision: complete this queue track. The next implementation should build the
  smallest repair dataset/profile for the two lanes and rerun the pinned suite.
