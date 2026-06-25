# Qwen3 v4 BFCL Text-Prefix Bridge 30-Case Smoke

- Status: `scored-repair-evidence-fail-closed`
- Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
- Model id: `Qwen/Qwen3-4B-Instruct-2507-FC`
- Run root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-bfcl-text-prefix-bridge-30-20260625`

## Runtime

BFCL used `/v1/completions` for generation. A direct chat probe returned native OpenAI `tool_calls`, so the new chat `reasoning_content` promotion path was not exercised by this BFCL run.

The scored 30-case run used:

```bash
scripts/openai_normalizing_proxy.py \
  --model-override Qwen/Qwen3-4B-MLX-4bit \
  --completion-prompt-suffix '<tool_call>' \
  --completion-reasoning-prefix '<tool_call>' \
  --completion-text-prefix '<tool_call>' \
  --chat-reasoning-tool-call-content
```

## Scores

| Metric | Score |
|---|---:|
| Overall Acc | 0.0033 |
| Non-Live Overall Acc | 0.0333 |
| simple_python AST | 0.100 |
| multiple AST | 0.100 |
| parallel AST | 0.000 |

## Row Audit

| Category | Rows | Blank | Visible tool | Reasoning content | Prose without tool |
|---|---:|---:|---:|---:|---:|
| simple_python | 10 | 1 | 1 | 9 | 8 |
| multiple | 10 | 4 | 1 | 9 | 5 |
| parallel | 10 | 2 | 1 | 9 | 7 |

## Decision

The text-prefix bridge is real repair evidence: the three-case smoke moved `simple_python_0` to 100%, and the 30-case slice produced nonzero `simple_python` and `multiple` scores. It is still nowhere near a BFCL pass. Parallel remains 0, most rows still hide tool-call-shaped content in `reasoning_content`, and many visible completions are prose rather than XML tool calls.

Next action: use the text-prefix bridge for further BFCL diagnostics, but prioritize targeted BFCL SFT or prompt-profile repair for visible XML tool-call completion, multi-call ordering, and prose suppression before running another full selected slice.

## Boundary

Selected 30-case BFCL repair evidence only. This is not a full BFCL leaderboard score, not a passing Hermes tool-call claim, and not a model publication gate pass.
