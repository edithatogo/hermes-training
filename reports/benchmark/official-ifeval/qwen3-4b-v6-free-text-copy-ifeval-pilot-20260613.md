# Qwen3 4B V6 Free-Text Copy Official IFEval Pilot

Date: 2026-06-13

## Identity

- Candidate: `qwen3-4b-strict-toolcall-v6-free-text-copy`
- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v6-free-text-copy/lora_adapter_iter125`
- Runtime: `mlx_lm.server` OpenAI-compatible chat endpoint
- Endpoint: `http://127.0.0.1:8080/v1/chat/completions`
- Benchmark env: `/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312`
- Harness: `lm_eval==0.4.12`
- Task: `ifeval`, task version `4`
- Scope: pilot-only, `--limit 25`

This is not a leaderboard score. The run uses a 25-sample limit to validate
the official harness path and compare instruction-following drift after the v6
strict tool-call repair.

## Runtime Command

```bash
source scripts/env.sh
./.venv/bin/mlx_lm.server \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter-path gemma4/experiments/qwen3-4b-strict-toolcall-v6-free-text-copy/lora_adapter_iter125 \
  --host 127.0.0.1 \
  --port 8080 \
  --temp 0 \
  --max-tokens 512 \
  --chat-template-args '{"enable_thinking":false}'
```

Important limitation: this endpoint run disables thinking through chat-template
args, but it does not inject the strict Hermes assistant-prefill profile used
by the local strict tool-call gate. Treat these IFEval results as endpoint
pilot evidence only.

## Benchmark Command

```bash
source scripts/env.sh
RUN_ID=qwen3-4b-v6-free-text-copy-ifeval-pilot-20260613
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ifeval/${RUN_ID}
mkdir -p "$OUT"

OPENAI_API_KEY=dummy \
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run \
  --model local-chat-completions \
  --model_args model=Qwen/Qwen3-4B-MLX-4bit,base_url=http://127.0.0.1:8080/v1/chat/completions,tokenizer=Qwen/Qwen3-4B,tokenizer_backend=huggingface,tokenized_requests=False,max_gen_toks=512,timeout=300 \
  --tasks ifeval \
  --limit 25 \
  --batch_size 1 \
  --apply_chat_template \
  --gen_kwargs temperature=0 \
  --output_path "$OUT" \
  --log_samples \
  --seed 0,1234,1234,1234
```

## Results

Raw output:

```text
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ifeval/qwen3-4b-v6-free-text-copy-ifeval-pilot-20260613
```

Result file:

```text
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ifeval/qwen3-4b-v6-free-text-copy-ifeval-pilot-20260613/Qwen__Qwen3-4B-MLX-4bit/results_2026-06-13T10-20-43.743311.json
```

| Metric | Value |
|---|---:|
| Samples | 25 |
| Prompt-level strict accuracy | 0.720 |
| Prompt-level loose accuracy | 0.800 |
| Instruction-level strict accuracy | 0.784 |
| Instruction-level loose accuracy | 0.865 |

## Decision

The v6 adapter remains a strict Hermes tool-call candidate, not a broad
instruction-following release. The bounded official IFEval pilot is slightly
below the prior v4 pilot on prompt-level strict accuracy (`0.720` vs `0.760`),
so the model card should keep broad instruction-following claims explicitly
out of scope.
