# EXAONE 4.0 1.2B Q4_K_M llama.cpp Smoke - 2026-06-12

## Summary

`mlx-community/exaone-4.0-1.2b-4bit` and
`LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF` were checked as the next small local model
lane. The MLX package is currently blocked in this environment before scoring,
while the official Q4_K_M GGUF loads and generates through llama.cpp.

This is runtime evidence only. The GGUF output was not compliant JSON.

## MLX Blocker

Artifact:

`/Volumes/PortableSSD/huggingface/hub/models--mlx-community--exaone-4.0-1.2b-4bit/snapshots/6dbf5f06dcb9526a7c328f692b1e08d35e17bff2`

Command:

```bash
./.venv/bin/python scripts/run_mlx_loglikelihood_smoke.py \
  --model /Volumes/PortableSSD/huggingface/hub/models--mlx-community--exaone-4.0-1.2b-4bit/snapshots/6dbf5f06dcb9526a7c328f692b1e08d35e17bff2 \
  --suite benchmarks/lm_loglikelihood/smoke.jsonl \
  --run-id exaone4-12b-mlx-loglikelihood-smoke-20260612 \
  --max-cases 1 \
  --max-length 1024
```

Result:

```text
ZeroDivisionError: division by zero
```

The failure occurs inside Transformers `configuration_exaone4.py` while
constructing the tokenizer/config for `mlx_lm.load`. Treat the MLX path as
blocked until the local Transformers/MLX stack handles this config.

## GGUF Runtime

Artifact:

- Repo: `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF`
- File: `EXAONE-4.0-1.2B-Q4_K_M.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--LGAI-EXAONE--EXAONE-4.0-1.2B-GGUF/snapshots/162446400ea4596377a3ce1d3ddffa32971af0a6/EXAONE-4.0-1.2B-Q4_K_M.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Acquisition note: one read timeout occurred and the Hugging Face client
  resumed the download successfully.

Command:

```bash
/opt/homebrew/bin/llama-completion \
  -m /Volumes/PortableSSD/huggingface/hub/models--LGAI-EXAONE--EXAONE-4.0-1.2B-GGUF/snapshots/162446400ea4596377a3ce1d3ddffa32971af0a6/EXAONE-4.0-1.2B-Q4_K_M.gguf \
  --ctx-size 512 \
  --n-predict 32 \
  --temp 0 \
  --seed 1 \
  --no-display-prompt \
  --no-conversation \
  --simple-io \
  --prompt 'Return only JSON: {"ok": true}'
```

Result:

```json
{
  "timed_out": false,
  "returncode": 0,
  "wall_time_s": 2.039,
  "max_rss_kb": 941473792,
  "stdout_tail": " } } } } } } } } } } } } } } } } } } } } } } } } } } } } } } } }\\n\\n"
}
```

Runtime metrics from llama.cpp stderr:

- Load time: `468.46 ms`
- Prompt eval: `213.18 tokens/s`
- Generation eval: `118.93 tokens/s`
- Total generation work: `320.42 ms / 40 tokens`

Runtime warning:

- `special_eos_id is not in special_eog_ids - the tokenizer config may be incorrect`

## Decision

- Status: `gguf-runtime-proofed; mlx-blocked; hermes-smoke-blocked`
- Do not promote to Hermes default, training, or publication.
- Next gate: use GGUF only as a small-runtime baseline, or retry MLX after the
  Transformers EXAONE4 config issue is fixed.
