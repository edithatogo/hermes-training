# Qwen3 v4 Official Candidate Execution Matrix

Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Queue source: `reports/benchmark/official-candidates/qwen3-v4-official-candidate-suite-queue-20260616.json`
Status: `scored-artifacts-present-repair-required`

No public broad benchmark claim until every required suite has scored artifacts and the scored gates pass, or until failures are explicitly excluded in publication materials.

| Suite | Queue | Execution | Blocker | Completion artifact |
|---|---|---|---|---|
| `official-bfcl` | `missing` | `scored-artifact-present` | BFCL selected-slice scored artifact exists; overall accuracy is 0.006 across simple_python,multiple,parallel. | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624/scores/data_overall.csv` |
| `official-coding` | `missing` | `scored-artifact-present` | EvalPlus scored artifact exists; HumanEval base pass@1 is 0.518 and HumanEval+ pass@1 is 0.482. | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-rerun-20260624/generated.jsonl and /Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-rerun-20260624/generated_eval_results.json` |
| `safety-refusal` | `missing` | `scored-artifact-present` | Scored artifact exists; strict pass rate is 0.125, so this is evidence for repair prioritization rather than a passing safety claim. | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616/summary.json` |
| `ruler-long-context` | `missing` | `scored-artifact-present` | Full RULER ctx4096 artifact exists; niah_single_1 4096 score is 1.000 over 500 samples. | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096 score summary` |

## Next Actions

### official-bfcl

- Next action: Treat the selected-slice BFCL result as scored-but-failing repair evidence. Prioritize parallel tool-call training and blank-output reduction before making any BFCL or Hermes tool-call capability claim.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624`

```bash
REMOTE_OPENAI_BASE_URL=http://127.0.0.1:8168/v1 REMOTE_OPENAI_API_KEY=EMPTY REMOTE_OPENAI_TOKENIZER_PATH=Qwen/Qwen3-4B LOCAL_SERVER_ENDPOINT=127.0.0.1 LOCAL_SERVER_PORT=8168 /Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl generate --model Qwen/Qwen3-4B-Instruct-2507-FC --test-category simple_python,multiple,parallel --temperature 0 --skip-server-setup --num-threads 1 --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624/results --include-input-log --allow-overwrite && /Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl evaluate --model Qwen/Qwen3-4B-Instruct-2507-FC --test-category simple_python,multiple,parallel --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624/results --score-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-text-prefix-selected-20260624/scores --partial-eval
```

### official-coding

- Next action: Inspect failed HumanEval tasks before making any broad coding claim.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-rerun-20260624`

```bash
source scripts/env.sh && EVALPLUS_MAX_MEMORY_BYTES=-1 /Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python -m evalplus.evaluate humaneval --samples /Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-rerun-20260624/generated.jsonl --test-details --parallel 8 --i-just-wanna-run
```

### safety-refusal

- Next action: Inspect residual refusal failures and add a repair track before public safety/refusal claims.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616`

```bash
./.venv/bin/python scripts/run_tool_call_benchmark.py --suite reports/benchmark/manifests/safety-refusal-suite-20260616.json --output-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616
```

### ruler-long-context

- Next action: Add longer-context RULER slices before making claims beyond ctx4096 needle retrieval.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616`

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run --model hf --model_args pretrained=Qwen/Qwen3-4B,peft=edithatogo/qwen3-4b-hermes-lora-peft-converted,trust_remote_code=True,dtype=float16,max_length=4096 --device mps --tasks niah_single_1 --batch_size 1 --metadata '{"max_seq_lengths":[4096]}' --output_path /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096
```

## Latest Safety Repair

- Selected runtime profile: `qwen3-v9-no-think-prefill-refusal-marker-normalized`
- Status: `runtime-profile-selected`
- Runtime-normalized v9 strict pass: `1.000`
- Raw v9 strict pass: `0.875`
- Raw v10 strict pass: `0.750`
- Report: `reports/benchmark/official-candidates/qwen3-v9-runtime-safety-refusal-profile-selection-20260624.json`
- Claim boundary: The passing result depends on runtime response normalization for one text-mode refusal. Raw v9 and v10 do not pass the pinned safety/refusal gate.
