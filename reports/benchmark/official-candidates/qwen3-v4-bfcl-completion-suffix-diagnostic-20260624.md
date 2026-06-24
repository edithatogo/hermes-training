# Qwen3 v4 BFCL Completion-Suffix Diagnostic

- Status: `runtime-bridge-ready-for-bounded-rerun`
- Proxy supports completion prompt suffix: `true`
- Proposed suffix: `<tool_call>`

## Evidence

| Run | Rows | Blank rows | Tool-like rows | Blank rate |
|---|---:|---:|---:|---:|
| Clean gated rerun | 10 | 10 | 0 | 1.000 |
| Serial partial without suffix | 383 | 320 | 0 | 0.836 |
| Tool-call prefix one-case gate | 1 | 1 | 0 | 1.000 |
| Reasoning bridge one-case gate | 1 | 1 | 0 | 1.000 |
| Capped512 partial | 119 | 7 | 0 | 0.059 |

## Decision

The clean endpoint/proxy path no longer shows upstream errors, but BFCL completions are whitespace-only when the completion prompt ends at the assistant marker. One-case prompt-prefix/reasoning bridge attempts and a capped512 partial still failed the blank gate, so the next bounded rerun must stop early unless the first 10-case suffix/profile gate produces nonblank tool-like rows.

## Gate

- Passed: `false`
- Reason: Runtime bridge is available, but the recorded micro-gates still fail blank-output checks.

## Boundary

Diagnostic/runtime-bridge evidence only. This does not create a BFCL score claim and does not change model weights.
