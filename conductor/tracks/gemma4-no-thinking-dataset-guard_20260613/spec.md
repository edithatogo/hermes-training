# Specification: Gemma 4 No-Thinking Dataset Guard

## Problem

The official Gemma 4 prompt-format guidance recommends adding an empty thought
channel when fine-tuning Gemma 4 26B A4B and 31B with no-thinking data. The repo
had documented the requirement, but the training configs did not yet have an
enforceable data path or readiness gate.

## Scope

- Add materialization and validation scripts at the hub level.
- Materialize Gemma-specific no-thinking datasets inside the nested `gemma4`
  repo without mutating shared Qwen/Hermes splits.
- Retarget the Gemma 4 26B A4B experimental configs to the Gemma-specific data.
- Add nested and hub Conductor evidence.

## Out Of Scope

- No Gemma 4 adapter training.
- No benchmark or promotion claim.
- No changes to Qwen3 v4 default Hermes selection.

## Acceptance Criteria

- Readiness validates Gemma 4 no-thinking data automatically.
- Unit tests cover materialization and validation.
- The nested `gemma4` repo is committed and pushed before the hub pointer moves.
- Project health remains `>= 9.5 / 10`.
