# Qwen3 v4 Official Candidate Suite Queue

Coverage source: `reports/benchmark/standard-coverage/qwen3-v4-targeted-standard-coverage-20260526.json`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
PEFT repo: `edithatogo/qwen3-4b-hermes-lora-peft-converted`

This queue keeps missing official-candidate suites executable without treating them as completed evidence.

| Suite | Status | Priority | Blocker | Next action |
|---|---:|---:|---|---|
| `official-bfcl` | `missing` | 10 | Needs a local OpenAI-compatible endpoint for the v4 PEFT adapter or a cloud endpoint that supports BFCL self-hosted generation. | Start the v4 adapter endpoint, then run the isolated BFCL env against simple_python,multiple,parallel before broad BFCL categories. |
| `official-coding` | `missing` | 20 | Needs an execution-enabled coding harness path; generation-only results must not be reported as pass@k. | Use EvalPlus/HumanEval/MBPP from the general benchmark env with execution enabled, or record the sandbox blocker explicitly. |
| `safety-refusal` | `missing` | 30 | Needs a pinned refusal/safety suite with expected refusal boundaries for unavailable or disallowed tools. | Materialize a versioned refusal suite from the held-out refusal cases plus unsafe-tool prompts, then score exact JSON refusal behavior. |
| `ruler-long-context` | `missing` | 40 | Needs a context-length decision and a RULER-compatible runtime path; local Mac runs may be slow or memory-bound. | Start with a small RULER needle/retrieval slice at the actual supported context length, then scale only if the runtime is stable. |

## Commands

### official-bfcl

- Run ID: `qwen3-v4-peft-official-bfcl-20260616`
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616`
- Publication boundary: No public broad benchmark claim until this suite has scored artifacts and review sign-off.

Local command:

```bash
REMOTE_OPENAI_BASE_URL=http://127.0.0.1:<port>/v1 REMOTE_OPENAI_API_KEY=EMPTY /Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl generate --model Qwen/Qwen3-4B-Instruct-2507-FC --test-category simple_python,multiple,parallel --temperature 0 --skip-server-setup --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/results --include-input-log && /Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl evaluate --model Qwen/Qwen3-4B-Instruct-2507-FC --test-category simple_python,multiple,parallel --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/results --score-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/scores --partial-eval
```

Cloud route: Route the same OpenAI-compatible endpoint command through a persistent backend only after its operator gate passes.

Completion criteria:
- BFCL generate returns 0
- BFCL evaluate returns 0
- score directory contains category summaries
- run card records endpoint, adapter revision, raw result root, and errors

### official-coding

- Run ID: `qwen3-v4-peft-official-coding-20260616`
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616`
- Publication boundary: No public broad benchmark claim until this suite has scored artifacts and review sign-off.

Local command:

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python -m evalplus.evaluate humaneval --samples /Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generated.jsonl --test-details
```

Cloud route: Use a persistent GPU/CPU container only after sandbox, result persistence, and cost gates are recorded.

Completion criteria:
- generated solutions are saved before execution
- test execution is enabled and recorded
- pass@1, compile errors, and timeouts are summarized
- run card records sandbox and raw generated solution paths

### safety-refusal

- Run ID: `qwen3-v4-peft-safety-refusal-20260616`
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616`
- Publication boundary: No public broad benchmark claim until this suite has scored artifacts and review sign-off.

Local command:

```bash
./.venv/bin/python scripts/run_tool_call_benchmark.py --suite reports/benchmark/manifests/safety-refusal-suite-20260616.json --output-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616
```

Cloud route: No cloud execution needed unless local runtime cannot serve the adapter reliably.

Completion criteria:
- suite manifest is versioned
- all refusal cases preserve plain-text no-tool-call refusals
- unsafe or unavailable tools are refused without leaking forbidden calls
- run card includes failure examples

### ruler-long-context

- Run ID: `qwen3-v4-peft-ruler-long-context-20260616`
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616`
- Publication boundary: No public broad benchmark claim until this suite has scored artifacts and review sign-off.

Local command:

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run --model hf --model_args pretrained=Qwen/Qwen3-4B,peft=edithatogo/qwen3-4b-hermes-lora-peft-converted,trust_remote_code=True,dtype=float16,max_length=4096 --device mps --tasks niah_single_1 --batch_size 1 --metadata '{"max_seq_lengths":[4096]}' --output_path /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096
```

Cloud route: Prefer Kaggle/Modal/Azure only after a persistent backend gate passes and the context length fits GPU memory.

Completion criteria:
- context length/task and tokenizer settings are recorded
- RULER task outputs are saved
- score summary includes task accuracy and context length
- run card records memory/runtime failures if blocked
