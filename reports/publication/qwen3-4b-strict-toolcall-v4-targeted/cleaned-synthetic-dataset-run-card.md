# Cleaned Synthetic Dataset Run Card

Date: 2026-05-26

## Decision

A cleaned synthetic-only dataset candidate has been materialized and audited
locally. Public dataset publication remains blocked pending explicit human
approval.

Generated JSONL files are stored on the SSD, outside the git repo:

```text
/Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526
```

## Materialization

Command:

```bash
python3 scripts/materialize_publication_dataset.py \
  --input-dir gemma4/data/strict_tool_call/expanded_splits_v4_targeted \
  --output-dir /Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526 \
  --summary-output /Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526/materialization-summary.json
```

Included source classes:

- `strict_tool_call_expansion_v1`
- `strict_tool_call_expansion_v2_format_guard`
- `strict_tool_call_expansion_v4_targeted`

Excluded source classes:

- `strict_tool_call_seed`
- `strict_tool_call`

Result:

| Split | Rows |
|---|---:|
| `train.jsonl` | 72 |
| `validation.jsonl` | 5 |
| `test.jsonl` | 5 |
| Total | 82 |

The generated dataset has `82` unique IDs and no duplicate IDs. The
materializer excluded `20` seed-derived rows from the original training split.

## Source Audit

Command:

```bash
source scripts/env.sh
./.venv/bin/python scripts/audit_publication_dataset_sources.py \
  /Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526 \
  --output reports/publication/qwen3-4b-strict-toolcall-v4-targeted/cleaned-synthetic-source-audit.json
```

Result:

| Source class | Rows |
|---|---:|
| `strict_tool_call_expansion_v1` | 54 |
| `strict_tool_call_expansion_v2_format_guard` | 16 |
| `strict_tool_call_expansion_v4_targeted` | 12 |

Unknown sources: `0`.

## Overlap And Structure Audit

Command:

```bash
source scripts/env.sh
./.venv/bin/python scripts/audit_tool_call_data.py \
  /Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526 \
  --benchmark-suite benchmarks/tool_call_local/suite.json \
  --heldout-suite benchmarks/tool_call_local/heldout_suite.json \
  --max-errors 100 \
  > reports/publication/qwen3-4b-strict-toolcall-v4-targeted/cleaned-synthetic-overlap-audit.json
```

Result:

| Check | Result |
|---|---|
| JSONL files | 3 |
| Rows | 82 |
| Unique IDs | 82 |
| Error count | 0 |
| Mirrored-suite user prompt overlap | 0 |
| Held-out-suite user prompt overlap | 0 |
| Held-out tool-name overlap | `notify_care_team` |

The remaining held-out overlap is a generic tool name only, not a held-out user
prompt.

## Token Audit

Command:

```bash
source scripts/env.sh
./.venv/bin/python scripts/dataset_token_audit.py \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --local-files-only \
  --data /Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526 \
  --splits train validation test \
  --output reports/publication/qwen3-4b-strict-toolcall-v4-targeted/cleaned-synthetic-token-audit.json
```

Result:

| Split | Rows | Tokens | Avg | P50 | P95 | Max |
|---|---:|---:|---:|---:|---:|---:|
| `train` | 72 | 17,145 | 238.1 | 246 | 347 | 360 |
| `validation` | 5 | 1,337 | 267.4 | 244 | 288 | 311 |
| `test` | 5 | 1,314 | 262.8 | 247 | 264 | 311 |

## Boundary

This run card proves a cleaned local candidate can be generated and audited.
It does not approve or perform a Hugging Face dataset publication.
