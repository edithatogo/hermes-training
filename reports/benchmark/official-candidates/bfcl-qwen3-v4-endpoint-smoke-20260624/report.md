# Qwen3 v4 BFCL Endpoint Smoke

Status: `passed-endpoint-and-partial-eval`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
BFCL model id: `Qwen/Qwen3-4B-Instruct-2507-FC`
Runtime model id: `Qwen/Qwen3-4B-MLX-4bit`
Adapter: `gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Endpoint: `mlx_lm.server` via `scripts/openai_normalizing_proxy.py`

This run proves that the v4 MLX adapter can be served behind an
OpenAI-compatible endpoint and consumed by BFCL. It is a three-case partial
evaluation only; it must not be described as a full official BFCL score.

## Result

| Category | Cases | Accuracy | Mean latency |
|---|---:|---:|---:|
| `simple_python` | 1 | `0.00%` | `12.52s` |
| `multiple` | 1 | `0.00%` | `12.54s` |
| `parallel` | 1 | `0.00%` | `8.18s` |
| Overall partial | 3 | `0.00%` | `11.08s` |

All three failures were `wrong_count` because the adapter returned blank
tool-call outputs (`"\n\n"` or `"\n\n\n"`). The endpoint and BFCL evaluator
were operational; the model behavior remains a repair target.

## Artifact Paths

- Smoke output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260624-smoke`
- Full-run attempt root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260624`
- Run-id input: `reports/benchmark/official-candidates/bfcl-qwen3-v4-endpoint-smoke-20260624/test_case_ids_to_generate.json`
- Overall score CSV: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260624-smoke/scores/data_overall.csv`

## Commands

```bash
source scripts/env.sh && .venv/bin/python -m mlx_lm.server \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter-path gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --host 127.0.0.1 --port 8097 --trust-remote-code \
  --temp 0 --max-tokens 512 \
  --chat-template-args '{"enable_thinking":false}'
```

```bash
source scripts/env.sh && .venv/bin/python scripts/openai_normalizing_proxy.py \
  --upstream http://127.0.0.1:8097/v1 \
  --listen-host 127.0.0.1 --listen-port 8098 \
  --timeout-s 600 \
  --model-override Qwen/Qwen3-4B-MLX-4bit
```

```bash
source scripts/env.sh && \
BFCL_PROJECT_ROOT=/Volumes/PortableSSD/GitHub/hermes-training/reports/benchmark/official-candidates/bfcl-qwen3-v4-endpoint-smoke-20260624 \
REMOTE_OPENAI_BASE_URL=http://127.0.0.1:8098/v1 \
REMOTE_OPENAI_API_KEY=EMPTY \
REMOTE_OPENAI_TOKENIZER_PATH=Qwen/Qwen3-4B \
LOCAL_SERVER_ENDPOINT=127.0.0.1 \
LOCAL_SERVER_PORT=8098 \
/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl generate \
  --model Qwen/Qwen3-4B-Instruct-2507-FC \
  --run-ids \
  --temperature 0 \
  --skip-server-setup \
  --num-threads 1 \
  --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260624-smoke/results \
  --include-input-log \
  --allow-overwrite
```

```bash
source scripts/env.sh && \
BFCL_PROJECT_ROOT=/Volumes/PortableSSD/GitHub/hermes-training/reports/benchmark/official-candidates/bfcl-qwen3-v4-endpoint-smoke-20260624 \
/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl evaluate \
  --model Qwen/Qwen3-4B-Instruct-2507-FC \
  --test-category simple_python,multiple,parallel \
  --result-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260624-smoke/results \
  --score-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260624-smoke/scores \
  --partial-eval
```

## Runtime Notes

- Direct BFCL use of `Qwen/Qwen3-4B-Instruct-2507-FC` against `mlx_lm.server`
  failed because the server attempted to resolve that model id as a Hugging
  Face repo.
- `scripts/openai_normalizing_proxy.py` now supports a scoped
  `--model-override` so BFCL can retain its registry id while the local MLX
  runtime receives `Qwen/Qwen3-4B-MLX-4bit`.
- A full 800-case BFCL run was attempted first with BFCL defaults, but the
  default high concurrency overloaded the single local MLX endpoint. It was
  interrupted after three `multiple` rows were written. The bounded smoke was
  rerun with `--num-threads 1`.
