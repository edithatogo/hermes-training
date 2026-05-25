---
license: apache-2.0
task_categories:
- text-generation
language:
- en
tags:
- hermes
- qwen3
- instruction-tuning
- tool-use
- synthetic-data
---

# Qwen3 Hermes Strict Tool-Call Synthetic V4

Publication status: blocked pending human scope approval.

## Dataset Summary

This draft describes the dataset scope used to train the public experimental
`qwen3-4b-hermes-lora` adapter. It is not a released Hugging Face dataset yet.

The current materialized training data lives in the repo at:

```text
gemma4/data/strict_tool_call/expanded_splits_v4_targeted
```

The recommended future public dataset should be a cleaned synthetic-only subset,
not a direct upload of the materialized training splits.

A cleaned synthetic-only candidate has been materialized locally but not
published:

```text
/Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526
```

## Intended Use

- Local supervised fine-tuning experiments for strict Hermes-style tool-call
  output.
- Regression testing for JSON validity, argument correctness, invalid-tool
  handling, and multi-turn repair formatting.
- Reproducibility companion material for the experimental Qwen3 v4 adapter.

## Not Intended For

- Broad claims about BFCL, IFEval, HumanEval, MBPP, or production tool-use
  performance.
- Training without the documented Qwen runtime prompt condition.
- Dataset contamination studies without reading the overlap audits.

## Current Materialized Composition

| Split file | Rows |
|---|---:|
| `train.jsonl` | 92 |
| `val.jsonl` | 5 |
| `valid.jsonl` | 5 |
| `test.jsonl` | 5 |

The materialized dataset has `107` rows, `102` unique IDs, and `46` rows with
`/no_think` prompt variants.

Source counts:

| Source class | Rows | Release posture |
|---|---:|---|
| `strict_tool_call_seed` | 10 | Exclude from future public dataset by default. |
| `strict_tool_call` | 10 | Exclude from future public dataset by default. |
| `strict_tool_call_expansion_v1` | 59 | Candidate for future cleaned synthetic release. |
| `strict_tool_call_expansion_v2_format_guard` | 16 | Candidate for future cleaned synthetic release. |
| `strict_tool_call_expansion_v4_targeted` | 12 | Candidate for future cleaned synthetic release. |

## Token Counts

Token audit for the current materialized v4 dataset:

```text
reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-token-audit.json
```

The adapter run card records:

- train rows: `92`
- validation rows: `5`
- training tokens processed: `37,936`
- train split token count: `24,331`

## Provenance

The expansion rows are repo-authored synthetic examples. The current
materialized splits also include mirrored local regression seed material and
`/no_think` prompt variants. For that reason, the direct materialized splits are
not recommended for public dataset release.

## Contamination And Audit Status

Recorded audits:

- source audit: `dataset-source-audit.json`
- overlap audit: `dataset-overlap-audit.json`
- redistribution review: `redistribution-review.md`
- scope decision: `dataset-publication-scope.md`

Known caveats:

- no held-out user-prompt overlap was found against
  `benchmarks/tool_call_local/heldout_suite.json`
- one generic held-out tool-name overlap was found: `notify_care_team`
- mirrored regression seed rows intentionally overlap the local mirrored
  regression suite and should not be used as independent held-out evidence

## Recommended Future Release Scope

Only publish a cleaned synthetic-only dataset after explicit approval. The
recommended included source classes are:

- `strict_tool_call_expansion_v1`
- `strict_tool_call_expansion_v2_format_guard`
- `strict_tool_call_expansion_v4_targeted`

The recommended excluded source classes are:

- `strict_tool_call_seed`
- `strict_tool_call`

The current cleaned candidate has `82` rows, no duplicate IDs, and no held-out
user-prompt overlap. Its run card is
`cleaned-synthetic-dataset-run-card.md`.

## Associated Adapter

Adapter repo:

```text
https://huggingface.co/edithatogo/qwen3-4b-hermes-lora
```

The adapter is released as an experimental local strict Hermes tool-call LoRA
with pilot-only benchmark positioning. Dataset publication remains separate.
