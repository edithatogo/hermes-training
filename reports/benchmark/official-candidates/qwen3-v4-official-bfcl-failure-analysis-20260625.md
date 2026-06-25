# Qwen3 v4 Official BFCL Failure Analysis - 2026-06-25

Candidate: `qwen3-4b-strict-toolcall-v4-targeted`

Source result:
`reports/benchmark/official-candidates/qwen3-v4-official-bfcl-result-20260624.json`

## Score Baseline

| Metric | Value |
| --- | ---: |
| BFCL selected overall | 0.0065 |
| Non-live overall | 0.0646 |
| simple_python AST | 0.265 |
| multiple AST | 0.170 |
| parallel AST | 0.000 |

## Failure Shape

| Category | Rows | Correct | Blank final | Final text no tool call | Hidden reasoning tool calls | Visible one-call invalid |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| simple_python | 400 | 106 | 116 | 171 | 287 | 7 |
| multiple | 200 | 34 | 92 | 70 | 162 | 4 |
| parallel | 200 | 0 | 33 | 106 | 139 | 61 |

The dominant failure is not subtle argument quality. Most failures decode as
zero BFCL calls because the final `result` is blank or natural language, even
when a `<tool_call>` appears in `reasoning_content`.

Parallel has a second blocker: visible tool-call rows usually emit only one call
when the task expects multiple calls.

## Decision

Targeted repair is worthwhile, but do not start with broad fine-tuning.

The first runtime/proxy extraction repair is now implemented behind
`scripts/openai_normalizing_proxy.py --chat-reasoning-tool-call-content`. It is
off by default and should be used only for a bounded BFCL repair rerun.

The next repair gate should:

- promote a valid `reasoning_content` `<tool_call>` into final result only when
  the final result is blank or natural language
- keep promotion constrained to syntactically valid tool calls
- rerun a small `simple_python,multiple` BFCL smoke to measure decoded-empty
  recovery
- add a parallel-specific profile requiring one `<tool_call>` block per requested
  action
- only then create SFT repair data for parallel multi-call count and visible
  value/type errors

## Claim Boundary

This is diagnostic repair planning only. The current scored BFCL selected-slice
result remains:

- overall `0.0065`
- non-live `0.0646`
- simple_python `0.265`
- multiple `0.170`
- parallel `0.000`

Do not make a BFCL or Hermes tool-calling capability claim from the current
candidate.
