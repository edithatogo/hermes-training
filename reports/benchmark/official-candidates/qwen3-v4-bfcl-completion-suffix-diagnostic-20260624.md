# Qwen3 v4 BFCL Completion-Suffix Diagnostic

- Status: `runtime-bridge-ready-for-bounded-rerun`
- Proxy supports completion prompt suffix: `true`
- Proposed suffix: `<tool_call>`

## Evidence

| Run | Rows | Blank rows | Tool-like rows | Blank rate |
|---|---:|---:|---:|---:|
| Clean gated rerun | 10 | 10 | 0 | 1.000 |
| Serial partial without suffix | 383 | 320 | 0 | 0.836 |

## Decision

The clean endpoint/proxy path no longer shows upstream errors, but BFCL completions are whitespace-only when the completion prompt ends at the assistant marker. The next bounded rerun should route /v1/completions through the proxy with --completion-prompt-suffix '<tool_call>' and stop after a small gate if outputs remain blank.

## Gate

- Passed: `false`
- Reason: Runtime bridge is ready for a bounded rerun, but no completion-suffix BFCL score is recorded yet.

## Boundary

Diagnostic/runtime-bridge evidence only. This does not create a BFCL score claim and does not change model weights.
