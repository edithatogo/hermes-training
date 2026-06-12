# Phi-4 Mini Instruct Transformers Runtime Blocker - 2026-06-13

## Summary

`microsoft/Phi-4-mini-instruct` was checked as a small practical local
fine-tune/runtime candidate for Hermes and mem0 extractor experimentation.

The local Transformers path failed before weight download, model load, or
generation. No benchmark cases were scored.

Status: `remote-code-import-blocked`.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_transformers_pilot_benchmark.py \
  --model microsoft/Phi-4-mini-instruct \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id phi4-mini-instruct-transformers-mps-fp16-strict-bfcl-pilot-20260613 \
  --device mps \
  --dtype float16 \
  --max-tokens 256 \
  --require-no-extra-tool-text \
  --trust-remote-code
```

## Failure

The model config loaded, but `AutoModelForCausalLM.from_pretrained(...)` failed
while importing the remote model implementation:

```text
ImportError: cannot import name 'SlidingWindowCache' from 'transformers.cache_utils'
```

The failing remote file was downloaded into the SSD-backed Hugging Face modules
cache:

`/Volumes/PortableSSD/huggingface/modules/transformers_modules/microsoft/Phi_hyphen_4_hyphen_mini_hyphen_instruct/cfbefacb99257ffa30c83adab238a50856ac3083/modeling_phi3.py`

## Decision

- Do not treat this as a model quality result.
- Do not promote or train this lane on the current environment.
- Retry only after one of:
  - Pinning a compatible Transformers revision that exposes `SlidingWindowCache`.
  - Patching/routing the remote implementation safely.
  - Acquiring a community GGUF/MLX runtime with a clean local smoke.
