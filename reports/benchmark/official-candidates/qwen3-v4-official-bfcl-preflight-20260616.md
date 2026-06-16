# Qwen3 v4 Official BFCL Preflight

Date: 2026-06-16T00:00:00+00:00
Status: `blocked-endpoint-preflight`
Suite: `official-bfcl`
Run ID: `qwen3-v4-peft-official-bfcl-20260616`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616`

This report is a launch gate for the official BFCL slice. It does not contain BFCL scores.

## Checks

| Check | Pass |
|---|---:|
| `queue_item_present` | `true` |
| `suite_status_missing` | `true` |
| `run_id_matches` | `true` |
| `output_root_ssd_backed` | `true` |
| `local_command_uses_bfcl_generate` | `true` |
| `local_command_uses_bfcl_evaluate` | `true` |
| `bfcl_cli_executable` | `true` |
| `endpoint_reachable` | `false` |

## Endpoint

- Base URL: `(not configured)`
- Status: `not-configured`
- Detail: REMOTE_OPENAI_BASE_URL was not set.
- Models: `(none)`

## BFCL CLI

- Path: `/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl`
- Present: `true`
- Executable: `true`
- Help/version line: `Usage: bfcl [OPTIONS] COMMAND [ARGS]...`

## Blockers

- OpenAI-compatible endpoint is not reachable/configured

## Command

```bash
REMOTE_OPENAI_BASE_URL=http://127.0.0.1:<port>/v1 REMOTE_OPENAI_API_KEY=EMPTY /Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl generate --model Qwen/Qwen3-4B-Instruct-2507-FC --test-category simple_python,multiple,parallel --temperature 0 --skip-server-setup --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/results --include-input-log && /Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl evaluate --model Qwen/Qwen3-4B-Instruct-2507-FC --test-category simple_python,multiple,parallel --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/results --score-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/scores --partial-eval
```

## Decision

Run official BFCL generate/evaluate only after endpoint_reachable is true; this preflight is not scored benchmark evidence.
Publication boundary: No public broad benchmark claim until this suite has scored artifacts and review sign-off.
