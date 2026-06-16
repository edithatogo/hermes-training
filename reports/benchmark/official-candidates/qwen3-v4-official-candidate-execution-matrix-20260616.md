# Qwen3 v4 Official Candidate Execution Matrix

Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Queue source: `reports/benchmark/official-candidates/qwen3-v4-official-candidate-suite-queue-20260616.json`
Status: `blocked-pending-scored-artifacts`

No public broad benchmark claim until every required suite has scored artifacts or an explicit exclusion.

| Suite | Queue | Execution | Blocker | Completion artifact |
|---|---|---|---|---|
| `official-bfcl` | `missing` | `blocked-preflight` | OpenAI-compatible endpoint is not reachable/configured | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/scores` |
| `official-coding` | `missing` | `blocked-preflight` | generated solutions JSONL is missing | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generated.jsonl and EvalPlus score output` |
| `safety-refusal` | `missing` | `ready-for-runtime` | Runtime/model execution is still required; no scored summary exists yet. | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616/summary.json` |
| `ruler-long-context` | `missing` | `blocked-preflight` | RULER module is not installed in the SSD benchmark environment | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096 score summary` |

## Next Actions

### official-bfcl

- Next action: Start the v4 adapter endpoint, then run the isolated BFCL env against simple_python,multiple,parallel before broad BFCL categories.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616`

```bash
REMOTE_OPENAI_BASE_URL=http://127.0.0.1:<port>/v1 REMOTE_OPENAI_API_KEY=EMPTY /Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl generate --model Qwen/Qwen3-4B-Instruct-2507-FC --test-category simple_python,multiple,parallel --temperature 0 --skip-server-setup --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/results --include-input-log && /Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl evaluate --model Qwen/Qwen3-4B-Instruct-2507-FC --test-category simple_python,multiple,parallel --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/results --score-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/scores --partial-eval
```

### official-coding

- Next action: Use EvalPlus/HumanEval/MBPP from the general benchmark env with execution enabled, or record the sandbox blocker explicitly.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616`

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python -m evalplus.evaluate humaneval --samples /Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generated.jsonl --test-details
```

### safety-refusal

- Next action: Run the pinned suite against the v4 adapter when local runtime is available.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616`

```bash
./.venv/bin/python scripts/run_tool_call_benchmark.py --suite reports/benchmark/manifests/safety-refusal-suite-20260616.json --output-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616
```

### ruler-long-context

- Next action: Start with a small RULER needle/retrieval slice at the actual supported context length, then scale only if the runtime is stable.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616`

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python -m ruler.run --model Qwen/Qwen3-4B --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter --tasks niah_single_1 --max_seq_length 4096 --output_dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096
```
