# Gemma 4 E2B IT QAT Mobile Transformers Load Failure - 2026-06-13

## Summary

`google/gemma-4-E2B-it-qat-mobile-transformers` was checked as the smallest
official Gemma 4 E2B reference artifact in the current runtime-proof queue.
The package is attractive for Mac-local Hermes work because its
`model.safetensors` file is about `2.46G`, much smaller than the full
`google/gemma-4-E2B-it` safetensors artifact.

The local load proof did not reach generation. The installed repo environment
uses `transformers 5.3.0`, and `AutoModelForImageTextToText` failed because
the local Transformers build does not recognize `model_type: gemma4`.

## Artifact

- Repo: `google/gemma-4-E2B-it-qat-mobile-transformers`
- Relevant files:
  - `config.json`
  - `processor_config.json`
  - `tokenizer_config.json`
- Config signal:
  - `model_type: gemma4`
  - `processor_class: Gemma4Processor`
  - Gemma quantization config with 2-bit, 4-bit, and 8-bit module groups
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`

## Command

```bash
source scripts/env.sh
./.venv/bin/python - <<'PY'
from transformers import AutoProcessor, AutoModelForImageTextToText

repo = "google/gemma-4-E2B-it-qat-mobile-transformers"
processor = AutoProcessor.from_pretrained(repo, cache_dir="/Volumes/PortableSSD/huggingface/hub")
model = AutoModelForImageTextToText.from_pretrained(
    repo,
    cache_dir="/Volumes/PortableSSD/huggingface/hub",
    torch_dtype="auto",
    low_cpu_mem_usage=True,
)
PY
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/runtime-smoke/gemma4-e2b-it-qat-mobile-transformers-load-smoke-20260613/summary.json`

## Result

```text
ValueError: The checkpoint you are trying to load has model type `gemma4` but Transformers does not recognize this architecture.
```

The processor loaded in about `10s`, but the model class failed before weight
loading or generation. No BFCL endpoint pilot was run.

## Decision

- Status: `runtime-support-blocked`
- Do not redownload or benchmark this lane until the local Transformers stack
  supports `gemma4`.
- Next proof should be an environment upgrade/source-install check for Gemma 4
  support, then a short text-generation smoke before any strict Hermes BFCL
  pilot.
