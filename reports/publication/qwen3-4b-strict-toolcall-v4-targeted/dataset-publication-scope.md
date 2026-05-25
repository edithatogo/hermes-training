# Dataset Publication Scope: Qwen3 4B Strict Tool-Call V4 Targeted

Date: 2026-05-26

## Decision

Public dataset publication remains blocked.

The adapter release is already approved with disclosed dataset caveats, but a
public Hugging Face dataset repo should not be created from the current
materialized v4 splits until the user explicitly approves the scope below.

## Current Dataset Under Review

```text
gemma4/data/strict_tool_call/expanded_splits_v4_targeted
```

The materialized dataset contains `107` rows, `102` unique IDs, and `46` rows
with `/no_think` prompt variants.

Split counts:

| Split file | Rows |
|---|---:|
| `train.jsonl` | 92 |
| `val.jsonl` | 5 |
| `valid.jsonl` | 5 |
| `test.jsonl` | 5 |

Source counts:

| Source class | Rows | Scope decision |
|---|---:|---|
| `strict_tool_call_seed` | 10 | Exclude from public dataset by default because it mirrors local regression seed material. |
| `strict_tool_call` | 10 | Exclude from public dataset by default because it is a `/no_think` variant of mirrored seed material. |
| `strict_tool_call_expansion_v1` | 59 | Candidate for public dataset after final review; repo-authored deterministic synthetic expansion. |
| `strict_tool_call_expansion_v2_format_guard` | 16 | Candidate for public dataset after final review; repo-authored deterministic format-guard expansion. |
| `strict_tool_call_expansion_v4_targeted` | 12 | Candidate for public dataset after final review; repo-authored targeted synthetic rows from failure analysis. |

## Recommended Safe Scope

If a public dataset release is approved later, publish a cleaned synthetic-only
dataset rather than the exact materialized training splits.

Recommended included sources:

- `strict_tool_call_expansion_v1`
- `strict_tool_call_expansion_v2_format_guard`
- `strict_tool_call_expansion_v4_targeted`

Recommended excluded sources:

- `strict_tool_call_seed`
- `strict_tool_call`
- any row copied, paraphrased, or mechanically transformed from held-out
  benchmark prompts
- any row that includes private, real, or user-specific data

Recommended release name:

```text
qwen3-hermes-strict-toolcall-synthetic-v4
```

Recommended status for the dataset card:

```text
public_dataset_release=blocked_pending_human_scope_approval
```

## Required Pre-Publication Steps

Before creating a Hugging Face dataset repo:

1. Materialize a cleaned synthetic-only dataset from the approved source classes.
2. Re-run source audit, overlap audit, token audit, and JSONL validation against
   the cleaned dataset.
3. Re-run overlap audit against both local mirrored and held-out benchmark
   suites.
4. Confirm the cleaned dataset does not include benchmark seed rows or held-out
   prompt variants.
5. Finalize the dataset card with exact source counts, split counts, token
   counts, intended use, limitations, and leakage caveats.
6. Get explicit human approval to publish the cleaned dataset scope.

## Current Evidence

- Source audit: `dataset-source-audit.json`
- Overlap audit: `dataset-overlap-audit.json`
- Token audit: `dataset-token-audit.json`
- Redistribution review: `redistribution-review.md`
- Dataset card draft: `hf-dataset-card-draft.md`
- Cleaned synthetic materialization run card:
  `cleaned-synthetic-dataset-run-card.md`
- Cleaned synthetic source audit: `cleaned-synthetic-source-audit.json`
- Cleaned synthetic overlap audit: `cleaned-synthetic-overlap-audit.json`
- Cleaned synthetic token audit: `cleaned-synthetic-token-audit.json`

## Boundary

This scope package does not publish data and does not change the current
Hugging Face adapter release. It is a release plan for a future cleaned dataset
artifact.
