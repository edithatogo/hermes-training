# Qwen3 4B V4 Targeted lm-eval Selected Smoke

Date: 2026-05-26

## Identity

- Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
- Runtime: `mlx_lm.server`
- Endpoint: `http://127.0.0.1:8080`
- Harness: `lm_eval==0.4.12`
- Tasks attempted: `arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande`
- Scope: limited smoke, `--limit 10`

## Runtime Proof

The endpoint started successfully and passed both `/v1/models` and a
non-streaming chat completion smoke.

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

## Attempted Chat-Completions Command

```bash
OPENAI_API_KEY=dummy \
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run \
  --model local-chat-completions \
  --model_args model=Qwen/Qwen3-4B-MLX-4bit,base_url=http://127.0.0.1:8080/v1/chat/completions,tokenizer=Qwen/Qwen3-4B,tokenizer_backend=huggingface,tokenized_requests=False,max_gen_toks=512,timeout=300 \
  --tasks arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande \
  --limit 10 \
  --batch_size 1 \
  --apply_chat_template \
  --gen_kwargs temperature=0 \
  --output_path /Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/qwen3-4b-v4-targeted-lm-eval-selected-smoke-20260526 \
  --log_samples \
  --seed 0,1234,1234,1234
```

Result: blocked before scoring. The selected tasks issue loglikelihood
requests, and `local-chat-completions` raises:

```text
NotImplementedError: Loglikelihood is not supported for chat completions. Consider using the completions API instead.
```

## Attempted Completions Probe

The endpoint supports `/v1/completions` for simple text generation when
`logprobs` is a boolean:

```bash
curl http://127.0.0.1:8080/v1/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen3-4B-MLX-4bit","prompt":"The capital of France is","temperature":0,"max_tokens":4,"logprobs":true}'
```

However, `lm_eval --model local-completions` still failed on
`arc_challenge --limit 2` because the harness/server combination closes the
connection during loglikelihood requests. The server log shows `mlx_lm.server`
rejecting `logprobs` when it is not a boolean:

```text
ValueError: logprobs must be of type <class 'bool'>
```

## Proxy Completions Bridge Rerun

After adding `/v1/completions` passthrough and integer-to-boolean `logprobs`
coercion to `scripts/openai_normalizing_proxy.py`, a bounded local rerun was
attempted against the proxy.

Proxy:

```bash
source scripts/env.sh
./.venv/bin/python scripts/openai_normalizing_proxy.py \
  --upstream http://127.0.0.1:8080/v1 \
  --listen-host 127.0.0.1 \
  --listen-port 8098 \
  --quiet
```

Probe:

```bash
source scripts/env.sh
RUN_ID=qwen3-4b-v4-targeted-lm-eval-proxy-completions-probe-20260526
OUT="$HERMES_EVAL_ROOT/standard-benchmarks/lm-eval/${RUN_ID}"
mkdir -p "$OUT"
OPENAI_API_KEY=dummy \
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run \
  --model local-completions \
  --model_args model=Qwen/Qwen3-4B-MLX-4bit,base_url=http://127.0.0.1:8098/v1/completions,tokenizer=Qwen/Qwen3-4B,tokenizer_backend=huggingface,tokenized_requests=False,max_gen_toks=512,timeout=300 \
  --tasks arc_challenge \
  --limit 1 \
  --batch_size 1 \
  --gen_kwargs temperature=0 \
  --output_path "$OUT" \
  --log_samples \
  --seed 0,1234,1234,1234
```

Raw probe log:

```text
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/qwen3-4b-v4-targeted-lm-eval-proxy-completions-probe-20260526/lm-eval-proxy-completions-probe.log
```

Result: still blocked before scoring. The proxy successfully forwards
`/v1/completions` and records `X-Hermes-Coerced-Logprobs-Count: 1`, but
`mlx_lm.server` returns logprobs in its current response shape:

```json
{"logprobs": {"content": [{"id": 12095, "logprob": -0.625}]}}
```

`lm_eval --model local-completions` expects legacy OpenAI-style echoed prompt
logprobs:

```text
choice["logprobs"]["token_logprobs"]
```

The rerun failed with:

```text
KeyError: 'token_logprobs'
```

Do not shim this by fabricating echoed prompt logprobs from generated-token
logprobs; that would produce invalid scores. The remaining fix needs a direct
MLX loglikelihood evaluator or an endpoint that returns true echoed prompt
token logprobs in the legacy shape expected by lm-eval.

## Decision

`lm-eval-selected` is no longer merely missing; it is blocked on a
true loglikelihood-compatible local runtime shim or direct evaluator adapter for MLX.
Do not report ARC/HellaSwag/TruthfulQA/Winogrande scores for this adapter from
the current `mlx_lm.server` endpoint.

IFEval remains the validated official-harness pilot because it is a generation
task and does not require loglikelihood scoring.
