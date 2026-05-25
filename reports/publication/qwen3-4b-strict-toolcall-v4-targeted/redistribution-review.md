# Redistribution Review: Qwen3 4B Strict Tool-Call V4 Targeted

Date: 2026-05-25

## Scope

Reviewed dataset:

```text
gemma4/data/strict_tool_call/expanded_splits_v4_targeted
```

Machine audit:

```bash
./.venv/bin/python scripts/audit_publication_dataset_sources.py \
  gemma4/data/strict_tool_call/expanded_splits_v4_targeted \
  --output reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-source-audit.json
```

Result:

```text
review_result=reviewed_with_caveats
adapter_release_source_gate=source_review_complete_with_disclosed_caveats
public_dataset_release=blocked_pending_human_scope_approval
```

## Source Summary

| Source class | Rows | Review decision |
|---|---:|---|
| `strict_tool_call_seed` | 10 | Repo-authored mirrored strict local benchmark seed; disclose benchmark-seed overlap. |
| `strict_tool_call` | 10 | No-think prompt variants of the repo-authored mirrored seed; disclose benchmark-seed overlap. |
| `strict_tool_call_expansion_v1` | 59 | Repo-authored deterministic synthetic expansion; no external corpus dependency identified. |
| `strict_tool_call_expansion_v2_format_guard` | 16 | Repo-authored deterministic synthetic format-guard expansion; no external corpus dependency identified. |
| `strict_tool_call_expansion_v4_targeted` | 12 | Repo-authored targeted synthetic rows from local failure analysis; no held-out prompt copying identified. |

The materialized v4 split has `107` rows, `102` unique IDs, and `46` rows with
the `/no_think` prompt variant.

## Caveats

- The original mirrored strict seed intentionally overlaps
  `benchmarks/tool_call_local/suite.json`; that suite is regression evidence
  only and is not used as the held-out publication gate.
- The overlap audit found no held-out user-prompt overlap against
  `benchmarks/tool_call_local/heldout_suite.json`.
- The overlap audit found one generic held-out tool-name overlap:
  `notify_care_team`.
- Public dataset publication remains blocked until human scope approval because
  publishing the raw training rows would expose the mirrored local benchmark
  seed and prompt variants as a dataset artifact.

## Decision

Dataset/source redistribution review for adapter-release purposes is complete
with caveats. This clears the adapter source-review gate and supports public
adapter publication with disclosure. It does not approve public dataset
publication.

Remaining public adapter release blockers:

- none; release approval is recorded in `release-decision.md`
