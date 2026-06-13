# Constrained Envelope Diagnostic Summary

- Run id: `nanbeige41-3b-heldout-constrained-envelope-20260614`
- Model: `Nanbeige/Nanbeige4.1-3B`
- Suite: `benchmarks/tool_call_local/heldout_suite.json`
- Source output: `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/nanbeige41-3b-heldout-strict-20260614`
- Raw pass rate: `0.125`
- Constrained pass rate: `0.375`
- Promotion allowed: `False`

This is runtime-wrapper diagnostic evidence only. It does not promote raw model output.

## Category Breakdown

| Category | Cases | Pass rate |
|---|---:|---:|
| argument_correctness | 2 | 0.000 |
| invalid_tool_handling | 2 | 0.500 |
| json_validity | 2 | 0.500 |
| multi_turn_repair | 2 | 0.500 |

## Cases

| Case | Envelope action | Pass | Reason |
|---|---|---:|---|
| `heldout-json-validity-inventory` | `selected-tool-calls` | `True` |  |
| `heldout-json-validity-parallel-logistics` | `selected-tool-calls` | `False` | tool-call output did not match the expected JSON schema |
| `heldout-argument-correctness-lab-order` | `stripped-thinking-only` | `False` | tool-call output did not match the expected JSON schema |
| `heldout-argument-correctness-billing` | `selected-tool-calls` | `False` | tool-call output did not match the expected JSON schema |
| `heldout-invalid-tool-handling-payroll` | `stripped-thinking-only` | `False` | response did not contain a refusal or clarification marker |
| `heldout-invalid-tool-handling-security` | `selected-refusal-sentence` | `True` |  |
| `heldout-multi-turn-repair-purchase-order` | `stripped-thinking-only` | `False` | tool-call output did not match the expected JSON schema |
| `heldout-multi-turn-repair-weather-alert` | `selected-tool-calls` | `True` |  |
