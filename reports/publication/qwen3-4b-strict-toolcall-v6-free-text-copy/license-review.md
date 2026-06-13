# License Review: Qwen3 4B Strict Tool-Call V6 Free-Text Copy

Date: 2026-06-13

## Base Model

- Model: `Qwen/Qwen3-4B-MLX-4bit`
- Declared license family: Apache-2.0 compatible based on the existing Qwen3
  track review and Hugging Face metadata checks used for prior Qwen3 adapter
  releases.

## Adapter Data

The v6 materialized training data is repo-authored strict tool-call synthetic
data. A cleaned synthetic-only candidate was materialized at:

```text
/Volumes/PortableSSD/hermes-evals/datasets/qwen3-v6-synthetic-only-20260613
```

The cleaned dataset excludes mirrored seed rows and v5 pilot-polish rows. It
contains these approved source classes:

- `strict_tool_call_expansion_v1`
- `strict_tool_call_expansion_v2_format_guard`
- `strict_tool_call_expansion_v4_targeted`
- `strict_tool_call_expansion_v6_free_text_copy`

## Decision

No license blocker is identified for local adapter evidence. Public release is
still gated on final model-card review and explicit human approval.
