# Qwen3 4B V4 Targeted Official IFEval Pilot

Date: 2026-05-26

## Identity

- Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
- Runtime: `mlx_lm.server` OpenAI-compatible chat endpoint
- Endpoint: `http://127.0.0.1:8080/v1/chat/completions`
- Benchmark env: `/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312`
- Harness: `lm_eval==0.4.12`
- Task: `ifeval`, task version `4`
- Scope: pilot-only, `--limit 25`

This is not a leaderboard score. The run uses a 25-sample limit to validate
the official harness path and get a cheap signal on instruction following.

## Runtime Command

```bash
source scripts/env.sh
./.venv/bin/mlx_lm.server \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter-path gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --host 127.0.0.1 \
  --port 8080 \
  --temp 0 \
  --max-tokens 512 \
  --chat-template-args '{"enable_thinking":false}'
```

Important limitation: this endpoint run disables thinking through chat-template
args, but it does not inject the strict Hermes assistant-prefill profile used by
the local strict tool-call gate. Treat these IFEval results as endpoint pilot
evidence only.

## Benchmark Command

```bash
source scripts/env.sh
RUN_ID=qwen3-4b-v4-targeted-ifeval-pilot-20260526
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

Before the run, the isolated benchmark env needed two IFEval optional
dependencies installed:

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python -m pip install langdetect immutabledict
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval validate --tasks ifeval
```

Validation result: `All tasks found and valid`.

## Results

Raw output:

```text
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ifeval/qwen3-4b-v4-targeted-ifeval-pilot-20260526
```

Result file:

```text
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ifeval/qwen3-4b-v4-targeted-ifeval-pilot-20260526/Qwen__Qwen3-4B-MLX-4bit/results_2026-05-26T00-30-55.263381.json
```

| Metric | Value |
|---|---:|
| Samples | 25 |
| Prompt-level strict accuracy | 0.760 |
| Prompt-level loose accuracy | 0.840 |
| Instruction-level strict accuracy | 0.811 |
| Instruction-level loose accuracy | 0.865 |

## Decision

The official IFEval harness path is now proven locally for the v4 adapter. This
is useful pilot evidence, but it is not a publication-quality standardized
score because it is limited to 25 samples and does not use the strict
assistant-prefill runtime profile.

Next IFEval step: run the full task only after deciding whether to build a
runtime shim that can preserve the required assistant prefill through the
OpenAI-compatible endpoint.
