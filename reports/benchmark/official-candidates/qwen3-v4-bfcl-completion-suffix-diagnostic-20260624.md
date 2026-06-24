# Qwen3 v4 BFCL Completion-Suffix Diagnostic

- Status: `runtime-bridge-ready-for-bounded-rerun`
- Proxy supports completion prompt suffix: `true`
- Proposed suffix: `<tool_call>`
- Direct proxy probe starts with tool call: `true`

## Evidence

| Run | Rows | Blank rows | Tool-like rows | Blank rate |
|---|---:|---:|---:|---:|
| Clean gated rerun | 10 | 10 | 0 | 1.000 |
| Serial partial without suffix | 383 | 320 | 0 | 0.836 |
| Tool-call prefix one-case gate | 1 | 1 | 0 | 1.000 |
| Reasoning bridge one-case gate | 1 | 1 | 0 | 1.000 |
| Direct proxy text-prefix probe | 1 | 0 | 1 | 0.000 |
| Capped512 partial | 119 | 7 | 0 | 0.059 |

## Decision

The clean endpoint/proxy path no longer shows upstream errors, but BFCL completions are whitespace-only when the completion prompt ends at the assistant marker. A direct BFCL-shaped completions probe now proves the proxy can restore a consumed <tool_call> prefix into visible choices[].text; the remaining gate is to rerun BFCL itself with this bridge and stop early unless generated result files contain nonblank tool-like rows.

## Gate

- Passed: `false`
- Reason: Runtime bridge is available and directly proven, but no bounded BFCL result file has passed the blank-output and parser gates yet.

## Boundary

Diagnostic/runtime-bridge evidence only. This does not create a BFCL score claim and does not change model weights.
