# Qwen3 v4 Official BFCL Result

Status: `scored-artifact-present`
Run ID: `qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Scope: selected official BFCL categories `simple_python,multiple,parallel` with partial evaluation enabled.

This is scored evidence for the selected local official-candidate BFCL slice only. It is not a full BFCL leaderboard claim, not a broad BFCL capability claim, and not a passing Hermes tool-call result.

## Runtime

- Server: `mlx_lm.server`
- Runtime model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
- Proxy: `scripts/openai_normalizing_proxy.py`
- Proxy bridge: model override plus `<tool_call>\n` completion suffix/text-prefix bridge
- BFCL model id: `Qwen/Qwen3-4B-Instruct-2507-FC`
- BFCL threads: `1`
- Completion max tokens cap: `128`

## Scores

| Metric | Value |
|---|---:|
| BFCL reported overall partial accuracy | `0.0065` |
| Non-live overall accuracy | `0.0646` |
| Python Simple AST | `0.2650` |
| Multiple AST | `0.1700` |
| Parallel AST | `0.0000` |
| Mean latency | `2.90s` |
| P95 latency | `4.35s` |

The selected run completed generation for all `800/800` rows with no endpoint-error pattern. Earlier reachability and local concurrency blockers were cleared by serving the v4 MLX adapter behind `/v1`, bounding the prompt cache, and running BFCL with `--num-threads 1`.

## Row Audit

| Category | Rows | Blank rows | Tool-call rows | Endpoint-error-like rows |
|---|---:|---:|---:|---:|
| `simple_python` | 400 | 116 | 113 | 0 |
| `multiple` | 200 | 92 | 38 | 0 |
| `parallel` | 200 | 33 | 61 | 0 |

## Artifacts

- Result root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624/results`
- Score root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624/scores`
- Overall CSV: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624/scores/data_overall.csv`
- Non-live CSV: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624/scores/data_non_live.csv`
- Generate log: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624/logs/bfcl-generate-text-prefix-selected.log`
- Evaluate log: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624/logs/bfcl-evaluate-text-prefix-selected.log`

## Next Action

Treat this as scored-but-failing repair evidence. Prioritize parallel tool-call training and blank-output reduction before making any BFCL or Hermes tool-call capability claim.
