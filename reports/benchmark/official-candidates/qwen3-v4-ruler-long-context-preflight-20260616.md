# Qwen3 v4 RULER Long-Context Preflight

Date: 2026-06-16T00:00:00+00:00
Status: `blocked-ruler-preflight`
Suite: `ruler-long-context`
Run ID: `qwen3-v4-peft-ruler-long-context-20260616`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616`

This report is a launch gate for the RULER long-context slice. It does not contain RULER scores.

## Context Decision

- Initial context: `4096`
- Context ladder: `[4096, 8192, 16384]`
- Task: `niah_single_1`
- Reason: Start with a bounded needle/retrieval smoke before scaling context length.

## Checks

| Check | Pass |
|---|---:|
| `queue_item_present` | `true` |
| `suite_status_missing` | `true` |
| `run_id_matches` | `true` |
| `output_root_ssd_backed` | `true` |
| `command_uses_ruler_module` | `true` |
| `command_uses_initial_context` | `true` |
| `command_omits_context_placeholder` | `true` |
| `command_writes_ctx4096` | `true` |
| `benchmark_python_present` | `true` |
| `ruler_module_present` | `false` |

## Runtime

- RULER module present: `false`
- Detail: ``

## Blockers

- RULER module is not installed in the SSD benchmark environment

## Command

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python -m ruler.run --model Qwen/Qwen3-4B --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter --tasks niah_single_1 --max_seq_length 4096 --output_dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096
```

## Decision

Install/prove a RULER-compatible runtime before running the ctx4096 stage; this preflight is not scored benchmark evidence.
Publication boundary: No public broad benchmark claim until this suite has scored artifacts and review sign-off.
