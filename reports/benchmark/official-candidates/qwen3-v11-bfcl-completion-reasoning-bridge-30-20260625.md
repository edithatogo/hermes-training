# Qwen3 v11 BFCL Completion-Reasoning Bridge 30-Case Smoke

Run ID: `qwen3-v11-bfcl-completion-reasoning-bridge-30-20260625`
Status: `proxy-implemented-output-unchanged`
Candidate: `qwen3-4b-strict-toolcall-v11-bfcl-selected-repair`

Private fail-closed runtime repair evidence only. This is not a BFCL leaderboard
score, not a passing Hermes tool-call claim, and not a model publication gate
pass.

## Runtime Change

Implemented and tested:

```bash
scripts/openai_normalizing_proxy.py --completion-reasoning-tool-call-text
```

The flag promotes a complete `/v1/completions` `reasoning_content`
`<tool_call>...</tool_call>` block into scored `text` when `text` is blank or
prose. Unit coverage and the proxy self-test pass.

## Scores

| Metric | Score |
|---|---:|
| Overall Acc | `0.0008` |
| Non-Live Overall Acc | `0.0083` |
| simple_python AST | `0.100` |
| multiple AST | `0.000` |
| parallel AST | `0.000` |

These are unchanged from the prior v11 30-case bridge run.

## Row Audit

| Category | Rows | Blank result | Visible tool | Reasoning tool | Prose no tool | Decoded empty |
|---|---:|---:|---:|---:|---:|---:|
| `simple_python` | `10` | `1` | `1` | `9` | `8` | `9` |
| `multiple` | `10` | `3` | `0` | `10` | `7` | `10` |
| `parallel` | `10` | `1` | `3` | `7` | `6` | `7` |

Parallel again had `3` rows with one visible decoded call that still failed the
wrong-count checker.

## Decision

The proxy-level completions reasoning promotion is implemented and locally
tested, but it did not alter BFCL's generated result shape. The blocker is now
below the normalizing proxy: either the BFCL OpenAI handler is reconstructing
`result` from fields after proxy normalization, or the relevant hidden tool-call
is not exposed as top-level completions `reasoning_content` in the response body
the proxy receives.

Next action: instrument the BFCL OpenAI handler or MLX completions response
mapping directly, then rerun only this 30-case smoke.

