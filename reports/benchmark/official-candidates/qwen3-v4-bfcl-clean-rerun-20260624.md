# Qwen3 v4 BFCL Clean Rerun

- Status: `blocked-blank-output-gate`
- Run root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-clean-rerun-20260624`
- Total generated rows: `10`
- Upstream-error rows: `0`
- Blank-output rows: `10`
- Completed-output rows: `0`
- Overall accuracy: `0.00%`

## Category Counts

| Category | Rows | Upstream errors | Blank outputs | Completed outputs |
|---|---:|---:|---:|---:|
| `multiple` | 10 | 0 | 10 | 0 |

## Gate

- Passed: `false`
- Reason: Clean rerun has no upstream errors, but generated blank model outputs.

## Boundary

Evidence-only clean-rerun attempt. Not a full BFCL claim and not sufficient for model publication.

## Next Action

Repair blank BFCL completion behavior before another selected-slice regeneration; keep endpoint/proxy command shape because upstream errors were cleared.
