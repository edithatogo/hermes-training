# lm-evaluation-harness Candidate Command Manifest

Date: 2026-05-24

## Purpose

Run a broader local comparability pass after a model clears runtime smoke and the local strict tool-call gate.

## Gate

- Candidate must have a stable endpoint or local adapter supported by `lm-evaluation-harness`.
- Candidate must have SSD-backed raw output roots.
- Candidate must have a run card with model revision, adapter revision, runtime version, prompt template, and sampling settings.

## Command

```bash
source scripts/env.sh
RUN_ID=<model>-lm-eval-candidate-<date>
MODEL_ID=<runtime_model_id>
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/${RUN_ID}
mkdir -p "$OUT"

/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run \
  --model local-chat-completions \
  --model_args model=Qwen/Qwen3-4B-MLX-4bit,base_url=http://127.0.0.1:8080/v1/chat/completions,tokenizer=Qwen/Qwen3-4B,tokenizer_backend=huggingface,tokenized_requests=False,max_gen_toks=512,timeout=300 \
  --tasks arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande \
  --batch_size 1 \
  --apply_chat_template \
  --gen_kwargs temperature=0 \
  --output_path "$OUT" \
  --log_samples \
  --seed 0,1234,1234,1234
```

Use the smoke manifest first with `LIMIT=10`. This candidate command is the next tier and should not run until adapter compatibility is confirmed.

## Result Card Schema

```json
{
  "run_id": "<model>-lm-eval-candidate-<date>",
  "suite": "lm-eval-candidate",
  "model": "<runtime_model_id>",
  "tasks": ["arc_challenge", "hellaswag", "truthfulqa_mc2", "gsm8k", "winogrande"],
  "raw_output": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/<run-id>",
  "harness_version": null,
  "normalized_scores": {},
  "known_failures": [],
  "publish_decision": "internal-candidate"
}
```

## Publication Boundary

Candidate results can inform model selection, but public claims require full harness metadata, deterministic rerun notes, and reviewer sign-off.
