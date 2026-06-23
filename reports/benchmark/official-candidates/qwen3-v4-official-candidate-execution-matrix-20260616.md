# Qwen3 v4 Official Candidate Execution Matrix

Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Queue source: `reports/benchmark/official-candidates/qwen3-v4-official-candidate-suite-queue-20260616.json`
Status: `blocked-pending-scored-artifacts`

No public broad benchmark claim until every required suite has scored artifacts or an explicit exclusion.

| Suite | Queue | Execution | Blocker | Completion artifact |
|---|---|---|---|---|
| `official-bfcl` | `missing` | `blocked-preflight` | OpenAI-compatible endpoint is not reachable/configured | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/scores` |
| `official-coding` | `missing` | `scored-artifact-present` | EvalPlus scored artifact exists; HumanEval base pass@1 is 0.518 and HumanEval+ pass@1 is 0.482. | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generated.jsonl and EvalPlus score output` |
| `safety-refusal` | `missing` | `scored-artifact-present` | Scored artifact exists; strict pass rate is 0.125, so this is evidence for repair prioritization rather than a passing safety claim. | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616/summary.json` |
| `ruler-long-context` | `missing` | `blocked-runtime` | The local lm_eval RULER path reached model initialization on MPS but did not reach inference. The active shell is not authenticated with Hugging Face, the Qwen/Qwen3-4B cache is incomplete, and the PEFT-converted adapter repo is not present in the active HF cache. The attempted download also used /Users/doughnut/.cache/huggingface instead of an SSD-backed Hugging Face cache path. | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096 score summary` |

## Next Actions

### official-bfcl

- Next action: Start the v4 adapter endpoint, then run the isolated BFCL env against simple_python,multiple,parallel before broad BFCL categories.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616`

```bash
REMOTE_OPENAI_BASE_URL=http://127.0.0.1:<port>/v1 REMOTE_OPENAI_API_KEY=EMPTY /Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl generate --model Qwen/Qwen3-4B-Instruct-2507-FC --test-category simple_python,multiple,parallel --temperature 0 --skip-server-setup --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/results --include-input-log && /Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl evaluate --model Qwen/Qwen3-4B-Instruct-2507-FC --test-category simple_python,multiple,parallel --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/results --score-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616/scores --partial-eval
```

### official-coding

- Next action: Inspect failed HumanEval tasks before making any broad coding claim.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616`

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python -m evalplus.evaluate humaneval --samples /Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generated.jsonl --test-details
```

### safety-refusal

- Next action: Inspect residual refusal failures and add a repair track before public safety/refusal claims.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616`

```bash
./.venv/bin/python scripts/run_tool_call_benchmark.py --suite reports/benchmark/manifests/safety-refusal-suite-20260616.json --output-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616
```

### ruler-long-context

- Next action: Set HF_HOME, HUGGINGFACE_HUB_CACHE, HF_XET_CACHE, and TRANSFORMERS_CACHE to /Volumes/PortableSSD-backed paths; authenticate or provide HF_TOKEN for the PEFT-converted adapter; prefetch Qwen/Qwen3-4B and the adapter; then rerun the same smoke before launching the full ctx4096 RULER slice.
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616`

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run --model hf --model_args pretrained=Qwen/Qwen3-4B,peft=edithatogo/qwen3-4b-hermes-lora-peft-converted,trust_remote_code=True,dtype=float16,max_length=4096 --device mps --tasks niah_single_1 --batch_size 1 --metadata '{"max_seq_lengths":[4096]}' --output_path /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096
```
