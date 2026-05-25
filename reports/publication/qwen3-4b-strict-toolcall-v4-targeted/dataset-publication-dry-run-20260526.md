# Dataset Publication Dry Run: dataset-publication-dry-run-20260526

Created: `2026-05-25T18:22:51.792847+00:00`
Status: `dry-run-only`
Publish actions performed: `false`
Intended Hugging Face dataset repo: `edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4`

## Dataset

- Path: `/Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526`
- Files: `test.jsonl, train.jsonl, validation.jsonl`
- Rows: `82`
- Unique IDs: `82`
- Duplicate IDs: `0`
- Review result: `reviewed_with_caveats`

## Splits

| Split file | Rows |
|---|---:|
| `test.jsonl` | 5 |
| `train.jsonl` | 72 |
| `validation.jsonl` | 5 |

## Sources

| Source | Rows |
|---|---:|
| `strict_tool_call_expansion_v1` | 54 |
| `strict_tool_call_expansion_v2_format_guard` | 16 |
| `strict_tool_call_expansion_v4_targeted` | 12 |

## Evidence

| File | Present |
|---|---:|
| `cleaned-synthetic-source-audit.json` | `true` |
| `cleaned-synthetic-overlap-audit.json` | `true` |
| `cleaned-synthetic-token-audit.json` | `true` |
| `hf-dataset-card-draft.md` | `true` |
| `dataset-publication-scope.md` | `true` |

## Audit Summary

- Overlap audit error count: `0`
- Held-out prompt overlap count: `0`
- Token audit model: `Qwen/Qwen3-4B-MLX-4bit`

## Blockers

- explicit human approval for the cleaned synthetic-only dataset scope is still required

## Required Approval

To publish later, record this exact approval after reviewing the scope:

```text
I approve publishing the cleaned synthetic-only dataset at /Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526 to Hugging Face dataset repo edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4.
```

This dry run did not call `hf repo create`, `hf upload`, or any other publishing command.
