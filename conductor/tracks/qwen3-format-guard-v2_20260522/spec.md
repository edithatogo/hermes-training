# Specification: Qwen3 Strict Format Guard V2

## Overview

Run the next Qwen3 4B local strict tool-call attempts using a small format-guard expansion and a follow-up `/no_think` training augmentation that target empty or malformed thinking wrappers without weakening benchmark strictness.

## Requirements

- Add non-heldout format-guard examples to the strict tool-call lane.
- Keep assistant targets as clean `<tool_call>` blocks or plain refusals only.
- Include explicit instructions that the model must not emit `<think>` or `</think>` tags.
- Materialize deterministic v2 splits under `gemma4/data/strict_tool_call/expanded_splits_v2`.
- Materialize deterministic v3 `/no_think` splits under `gemma4/data/strict_tool_call/expanded_splits_v3_no_think` when v2 fails to remove the wrapper.
- Audit v2 raw data and splits for held-out contamination.
- Audit v3 splits for held-out contamination.
- Train local Qwen3 4B MLX LoRA adapters on v2 and v3 splits.
- Evaluate the adapters against mirrored and held-out strict suites with `/no_think`.
- Keep Hugging Face publication blocked unless strict held-out pass rate is `1.000`.

## Acceptance Criteria

- `raw/expansion_seed_v2.jsonl` exists and has zero held-out overlap.
- `expanded_splits_v2/{train,val,valid,test}.jsonl` exists.
- `expanded_splits_v3_no_think/{train,val,valid,test}.jsonl` exists.
- `scripts/train_config.qwen3-4b.strict-toolcall-v2.yaml` exists.
- `scripts/train_config.qwen3-4b.strict-toolcall-v3-no-think.yaml` exists.
- Training and held-out evaluation are recorded in docs for both attempts.
- Strict scoring remains unchanged.

## Out Of Scope

- Publishing adapters or datasets to Hugging Face.
- Changing strict benchmark pass semantics.
- Downloading larger models.
