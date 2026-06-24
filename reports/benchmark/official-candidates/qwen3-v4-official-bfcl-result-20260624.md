# Qwen3 v4 Official BFCL Result

Status: `scored-artifact-present`
Run ID: `qwen3-v4-peft-official-bfcl-20260616`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Scope: selected official BFCL categories `simple_python,multiple,parallel` with partial evaluation enabled.

This is scored evidence for the selected local official-candidate BFCL slice only. It is not a full BFCL leaderboard claim and must not be reported as broad BFCL capability.

## Runtime

- Server: `mlx_lm.server`
- Runtime model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
- Proxy: `scripts/openai_normalizing_proxy.py`
- BFCL model id: `Qwen/Qwen3-4B-Instruct-2507-FC`

## Scores

| Metric | Value |
|---|---:|
| Overall selected-slice accuracy | `0.000` |
| Python Simple AST | `0.000` |
| Multiple AST | `0.000` |
| Parallel AST | `0.000` |
| Mean latency | `95.24s` |
| P95 latency | `101.33s` |

BFCL reported that all selected test cases had been previously generated for `Qwen/Qwen3-4B-Instruct-2507-FC`; this run refreshed evaluation against the score files under the `20260616` official-candidate root.

## Artifacts

- Result root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/results`
- Score root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/scores`
- Overall CSV: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/scores/data_overall.csv`
- Generate log: `reports/benchmark/official-candidates/logs/qwen3-v4-official-bfcl-generate-20260624.log`
- Evaluate log: `reports/benchmark/official-candidates/logs/qwen3-v4-official-bfcl-evaluate-20260624.log`

## Next Action

Treat the `0.000` selected-slice BFCL score as a repair target. Inspect raw BFCL outputs and create a runtime/profile or adapter repair track before making any BFCL claim.
