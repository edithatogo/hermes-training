# Qwen3 v4 Official Coding Preflight

Date: 2026-06-23T17:23:02.506008+00:00
Status: `blocked-coding-preflight`
Suite: `official-coding`
Run ID: `qwen3-v4-peft-official-coding-20260616`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616`

This report is a launch gate for HumanEval/EvalPlus execution. It does not contain pass@k scores.

## Checks

| Check | Pass |
|---|---:|
| `queue_item_present` | `true` |
| `suite_status_missing` | `true` |
| `run_id_matches` | `true` |
| `output_root_ssd_backed` | `true` |
| `command_uses_evalplus_module` | `true` |
| `command_uses_positional_humaneval` | `true` |
| `command_uses_samples` | `true` |
| `command_omits_stale_model_flag` | `true` |
| `evalplus_cli_executable` | `true` |
| `evalplus_module_present` | `true` |
| `human_eval_module_present` | `true` |
| `generated_solutions_present` | `false` |

## Generated Solutions

- Path: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generated.jsonl`
- Present: `false`
- Rows: `0`
- Valid JSONL: `false`
- Error: generated solutions JSONL is missing

## EvalPlus

- CLI: `/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/evalplus.evaluate`
- Present: `true`
- Executable: `true`
- Help line: `INFO: Showing help with the command 'evalplus.evaluate -- --help'.`

## Blockers

- generated solutions JSONL is missing

## Command

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python -m evalplus.evaluate humaneval --samples /Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generated.jsonl --test-details
```

## Decision

Generate solutions first, then run EvalPlus with execution enabled; this preflight is not scored benchmark evidence.
Publication boundary: No public broad benchmark claim until this suite has scored artifacts and review sign-off.
