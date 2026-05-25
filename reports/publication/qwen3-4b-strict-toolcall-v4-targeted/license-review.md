# License Review: Qwen3 4B Strict Tool-Call V4 Targeted

Review date: 2026-05-25

## Scope

- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter candidate: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
- Dataset candidate: `gemma4/data/strict_tool_call/expanded_splits_v4_targeted`
- Benchmark gate: `benchmarks/tool_call_local/heldout_suite.json`

## Findings

- Hugging Face API reports `Qwen/Qwen3-4B-MLX-4bit` license as Apache-2.0.
- Hugging Face API reports `Qwen/Qwen3-4B` license as Apache-2.0.
- V4 targeted rows are hand-authored synthetic examples for exact message
  extraction and nested object-array JSON formatting.
- The materialized V4 split inherits the earlier strict tool-call seed and
  expanded rows.
- The dataset overlap audit found no held-out user-prompt overlap and one
  held-out tool-name overlap: `notify_care_team`.
- The held-out strict suite IDs and user prompts were not added to the targeted
  V4 training rows.

## Current Decision

GitHub source publication is acceptable for code, configs, run cards, and small
reproducibility artifacts.

Public Hugging Face adapter publication is not yet approved in this review.
Although the quality gate now passes, public publication still needs:

- final redistribution review for all materialized training rows inherited by V4
- finalized model card with the required assistant-prefill runtime condition
- human publication approval

Merged weights and GGUF publication remain out of scope for this adapter review.
