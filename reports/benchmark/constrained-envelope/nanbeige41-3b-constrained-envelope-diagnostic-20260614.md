# Constrained Envelope Diagnostic Summary

- Run id: `nanbeige41-3b-constrained-envelope-diagnostic-20260614`
- Model: `Nanbeige/Nanbeige4.1-3B`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/nanbeige-nanbeige4-1-3b-strict-suffix-copy-exact-20260614-021619`
- Raw pass rate: `0.000`
- Constrained pass rate: `1.000`
- Promotion allowed: `False`

This is runtime-wrapper diagnostic evidence only. It does not promote raw model output.

## Category Breakdown

| Category | Cases | Pass rate |
|---|---:|---:|
| contains_excludes | 1 | 1.000 |
| tool_call_exact | 2 | 1.000 |

## Cases

| Case | Envelope action | Pass | Reason |
|---|---|---:|---|
| `bfcl-simple-customer-lookup` | `selected-tool-calls` | `True` |  |
| `bfcl-parallel-ticket-routing` | `selected-tool-calls` | `True` |  |
| `bfcl-invalid-tool` | `selected-refusal-sentence` | `True` |  |
