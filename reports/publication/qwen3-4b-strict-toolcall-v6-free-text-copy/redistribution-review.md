# Redistribution Review: Qwen3 4B Strict Tool-Call V6 Free-Text Copy

Date: 2026-06-13

## Materialized Training Data

Training used:

```text
gemma4/data/strict_tool_call/expanded_splits_v6_free_text_copy
```

The full materialized splits include mirrored local-regression seed rows and
v5 pilot-polish rows. Those are acceptable for local evidence but should not be
published as a public dataset by default.

## Cleaned Synthetic-Only Dataset Candidate

The publication-scope dataset candidate is:

```text
/Volumes/PortableSSD/hermes-evals/datasets/qwen3-v6-synthetic-only-20260613
```

It contains `98` unique rows:

| Source class | Rows |
|---|---:|
| `strict_tool_call_expansion_v1` | 54 |
| `strict_tool_call_expansion_v2_format_guard` | 16 |
| `strict_tool_call_expansion_v4_targeted` | 12 |
| `strict_tool_call_expansion_v6_free_text_copy` | 16 |

The overlap audit reports zero structural errors and no held-out user-prompt
overlap. A generic inherited held-out tool-name overlap remains disclosed.

## Decision

Adapter release source gate: source review complete with disclosed caveats.
Public dataset release remains blocked pending explicit human scope approval.
