# Qwen3 v4 RULER Long-Context Preflight

Date: 2026-06-16T14:33:36.309630+00:00
Status: `ready-to-run`
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
| `command_uses_lm_eval` | `true` |
| `command_uses_ruler_task` | `true` |
| `command_uses_mps_device` | `true` |
| `command_uses_initial_context` | `true` |
| `command_omits_context_placeholder` | `true` |
| `command_writes_ctx4096` | `true` |
| `benchmark_python_present` | `true` |
| `lm_eval_ruler_tasks_present` | `true` |

## Runtime

- lm_eval RULER tasks present: `true`
- Detail: ``

## Blockers

- none

## Command

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run --model hf --model_args pretrained=Qwen/Qwen3-4B,peft=edithatogo/qwen3-4b-hermes-lora-peft-converted,trust_remote_code=True,dtype=float16,device=mps --tasks niah_single_1 --batch_size 1 --output_path /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096
```

## Decision

Use the installed lm_eval RULER task path before running the ctx4096 stage; this preflight is not scored benchmark evidence.
Publication boundary: No public broad benchmark claim until this suite has scored artifacts and review sign-off.
