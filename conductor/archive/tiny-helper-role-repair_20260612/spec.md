# Specification: Tiny Helper Role Repair

## Overview

Establish the best strict Hermes-compatible helper lane among the smallest
local models that are plausible on a MacBook Pro M1 with 32 GB unified memory.
The focus is not broad model coverage. It is to compare the tiny helper
candidates that already have live runtime evidence and then repair or normalize
their prompt format so the repo has a clear, documented helper/extraction lane.

Primary candidates:

- `openbmb/MiniCPM5-1B`
- `Qwen/Qwen3.5-0.8B`
- `Qwen/Qwen3.5-2B`

Secondary comparison lane:

- `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF`

## Goals

- Confirm the exact runtime IDs and packaging lane for each tiny candidate.
- Compare strict Hermes tool-call behavior, helper/extraction usefulness, and
  runtime ergonomics.
- Repair or normalize the prompt profile for the strongest tiny helper lane.
- Keep the result grounded in local evidence, not speculative promotion.
- Record the outcome in the maintained radar and handoff docs.

## Functional Requirements

1. Verify the current candidate set in `MODEL_CANDIDATES.yaml`.
2. Run or record bounded strict-format helper smokes for the candidate set.
3. Identify which candidate is best suited to Hermes helper/extraction work.
4. Add any prompt/profile repair or scoring wrapper needed to make the role
   explicit and reproducible.
5. Document the results in the benchmark and handoff bundle.
6. Keep all work scoped to local or Colab-appropriate execution paths.

## Non-Functional Requirements

- Prefer SSD-backed caches and artifact paths.
- Avoid unnecessary large-model downloads or training runs.
- Keep publication claims limited to the evidence actually produced.
- Preserve the repo's conductor-first layout and traceability.

## Acceptance Criteria

- The helper lane is explicit in the model radar and handoff notes.
- The candidate comparison is documented with concrete runtime evidence.
- Any prompt/profile repair is tracked in a report and reflected in the docs.
- The result clearly states whether the lane is runtime-only, helper-ready, or
  still blocked.
- Validation passes.

## Out of Scope

- Full leaderboard benchmarking.
- Large-model fine-tuning.
- Teacher-only frontier model promotion.
- Publishing adapters or merged weights.
