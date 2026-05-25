# lm-evaluation-harness Smoke Command Manifest

Date: 2026-05-24

## Purpose

Run a cheap engineering smoke before broader lm-eval execution.

## Command

```bash
source scripts/env.sh
RUN_ID=qwen3-4b-v4-targeted-lm-eval-selected-smoke-<date>
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/${RUN_ID}
mkdir -p "$OUT"

OPENAI_API_KEY=dummy \
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run \
  --model local-chat-completions \
  --model_args model=Qwen/Qwen3-4B-MLX-4bit,base_url=http://127.0.0.1:8080/v1/chat/completions,tokenizer=Qwen/Qwen3-4B,tokenizer_backend=huggingface,tokenized_requests=False,max_gen_toks=512,timeout=300 \
  --tasks arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande \
  --limit 10 \
  --batch_size 1 \
  --apply_chat_template \
  --gen_kwargs temperature=0 \
  --output_path "$OUT" \
  --log_samples \
  --seed 0,1234,1234,1234
```

## Artifact Root

```text
$HERMES_EVAL_ROOT/lm-eval/<run-id>
```

## Boundary

Limited-sample results are engineering smoke only. Do not publish them as benchmark scores.
