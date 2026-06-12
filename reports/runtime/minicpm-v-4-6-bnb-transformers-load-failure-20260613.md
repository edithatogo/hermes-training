# MiniCPM-V 4.6 BNB Transformers Load Failure - 2026-06-13

## Summary

`openbmb/MiniCPM-V-4.6-BNB` was checked as the next lightweight local-runtime
candidate in the Hermes proof queue. The model is a small BNB-quantized
MiniCPM-V 4.6 package with a `model.safetensors` file of about `1.06G`.

The local load proof did not reach generation. The installed repo environment
uses `transformers 5.3.0`, and both `AutoModelForImageTextToText` and
`AutoModelForCausalLM` failed because the local Transformers build does not
recognize `model_type: minicpmv4_6`.

This proof intentionally avoided pulling the full weight file after confirming
that the failure occurs at config/model-class resolution.

## Artifact

- Repo: `openbmb/MiniCPM-V-4.6-BNB`
- Large file: `model.safetensors`, about `1.06G`
- Config signal:
  - `model_type: minicpmv4_6`
  - `architectures: ["MiniCPMV4_6ForConditionalGeneration"]`
  - `processor_class: MiniCPMV4_6Processor`
  - `quant_method: bitsandbytes`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`

SSD output:

`/Volumes/PortableSSD/hermes-evals/runtime-smoke/minicpm-v-4-6-bnb-transformers-load-smoke-20260613/summary.json`

## Command

```bash
source scripts/env.sh
./.venv/bin/python - <<'PY'
from transformers import AutoModelForCausalLM, AutoModelForImageTextToText, AutoProcessor

repo = "openbmb/MiniCPM-V-4.6-BNB"
processor = AutoProcessor.from_pretrained(
    repo,
    cache_dir="/Volumes/PortableSSD/huggingface/hub",
    trust_remote_code=True,
)
for cls in [AutoModelForImageTextToText, AutoModelForCausalLM]:
    model = cls.from_pretrained(
        repo,
        cache_dir="/Volumes/PortableSSD/huggingface/hub",
        trust_remote_code=True,
        torch_dtype="auto",
        low_cpu_mem_usage=True,
    )
PY
```

## Result

Both auto model classes failed with:

```text
ValueError: The checkpoint you are trying to load has model type `minicpmv4_6` but Transformers does not recognize this architecture.
```

No generation smoke or strict Hermes BFCL endpoint pilot was run.

## Decision

- Status: `runtime-support-blocked`
- Do not redownload or benchmark this BNB lane until the local Transformers
  stack supports `minicpmv4_6`, or a supported GGUF/MLX/LiteRT runtime is used.
- If MiniCPM-V 4.6 remains important for multimodal helper workflows, prefer a
  GGUF/LiteRT path or a temporary source/nightly Transformers environment on
  the SSD.
