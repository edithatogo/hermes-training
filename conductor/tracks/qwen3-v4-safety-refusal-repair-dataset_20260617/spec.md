# Specification: Qwen3 v4 Safety/Refusal Repair Dataset

## Overview

Materialize a bounded v7 repair dataset and MLX training config for the Qwen3
v4 safety/refusal failures. This track turns the repair queue into concrete
training inputs without launching a fine-tune.

## Goals

- Build from `expanded_splits_v6_free_text_copy` without overwriting earlier
  splits.
- Add non-heldout examples for the two repair lanes:
  strict empty-think wrapper removal and forbidden-name refusal suppression.
- Keep validation and test splits unchanged from v6.
- Add a dedicated v7 training config that writes to a new adapter path.
- Validate the dataset, config, lane counts, no held-out IDs, no assistant
  thinking tags, and refusal targets that do not echo forbidden markers.

## Acceptance Criteria

- Add `gemma4/data/strict_tool_call/tools/materialize_safety_refusal_repair_splits_v7.py`.
- Materialize `gemma4/data/strict_tool_call/expanded_splits_v7_safety_refusal_repair/`.
- Add `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v7-safety-refusal-repair.yaml`.
- Add `scripts/validate_safety_refusal_repair_dataset.py`.
- Add focused unit tests.
- Update the strict tool-call expansion notes.
- Wire the validator into `scripts/validate_readiness.py`.
- Add this Conductor track to the registry.

## Out Of Scope

- Running the v7 training job.
- Promoting a new adapter.
- Rerunning the safety/refusal benchmark.
- Claiming standardized safety/refusal performance.
