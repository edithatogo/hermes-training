# Gemma 4 No-Thinking Dataset Materialization - 2026-06-13

## Purpose

Gemma 4 26B A4B and 31B no-thinking fine-tunes need an empty thought channel at
the start of model turns. The shared Hermes/Qwen splits were left unchanged, and
Gemma-specific copies were materialized for Gemma 4 training configs.

## Outputs

| Source | Target | Rows |
|---|---|---:|
| `gemma4/data/splits` | `gemma4/data/gemma4_no_thinking/splits` | 635 |
| `gemma4/data/strict_tool_call/expanded_splits_v6_free_text_copy` | `gemma4/data/gemma4_no_thinking/expanded_splits_v6_free_text_copy` | 131 |

## Empty Channel

Assistant messages in the Gemma-specific datasets now start with:

```text
<|channel>thought
<channel|>
```

## Config Changes

- `gemma4/scripts/train_config.gemma4-26b-a4b.experimental.yaml` now points at
  `data/gemma4_no_thinking/splits`.
- `gemma4/scripts/train_config.gemma4-26b-a4b.free-text-copy.experimental.yaml`
  now points at `data/gemma4_no_thinking/expanded_splits_v6_free_text_copy`.
- Both configs set `gemma4_no_thinking_empty_channel: true`.

## Validation

- `scripts/materialize_gemma4_no_thinking_dataset.py` materializes the datasets.
- `scripts/validate_gemma4_no_thinking_dataset.py` validates Gemma 4 26B/31B
  configs and dataset rows.
- `scripts/validate_readiness.py` now runs the validator as part of the global
  readiness gate.
