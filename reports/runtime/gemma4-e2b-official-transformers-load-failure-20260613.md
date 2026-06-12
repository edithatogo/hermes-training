# Gemma 4 E2B Official Transformers Load Failure - 2026-06-13

## Summary

`google/gemma-4-E2B` and `google/gemma-4-E2B-it` were checked as the official
Gemma 4 E2B Hugging Face Transformers reference lanes at the top of the local
runtime-proof queue.

Both packages are blocked by the same local runtime-support issue seen in the
QAT Mobile package. The installed repo environment uses `transformers 5.3.0`,
and `AutoModelForImageTextToText` does not recognize `model_type: gemma4`.

This proof intentionally avoided downloading the full `10.25G` safetensors
artifact for each official lane because the failure happens at config/model
class resolution before weight loading.

## Artifacts

| Repo | Large weight file | Result |
|---|---:|---|
| `google/gemma-4-E2B` | `model.safetensors`, about `10.25G` | processor loaded, model class failed before weight loading |
| `google/gemma-4-E2B-it` | `model.safetensors`, about `10.25G` | processor loaded, model class failed before weight loading |

SSD output:

`/Volumes/PortableSSD/hermes-evals/runtime-smoke/gemma4-e2b-official-transformers-load-smoke-20260613/summary.json`

## Command

```bash
source scripts/env.sh
./.venv/bin/python - <<'PY'
from transformers import AutoModelForImageTextToText, AutoProcessor

for repo in ["google/gemma-4-E2B", "google/gemma-4-E2B-it"]:
    processor = AutoProcessor.from_pretrained(repo, cache_dir="/Volumes/PortableSSD/huggingface/hub")
    model = AutoModelForImageTextToText.from_pretrained(
        repo,
        cache_dir="/Volumes/PortableSSD/huggingface/hub",
        torch_dtype="auto",
        low_cpu_mem_usage=True,
    )
PY
```

## Result

Both lanes failed with:

```text
ValueError: The checkpoint you are trying to load has model type `gemma4` but Transformers does not recognize this architecture.
```

No generation smoke or BFCL endpoint pilot was run.

## Decision

- Status: `runtime-support-blocked`
- Do not download the full official Gemma 4 E2B/E2B-it weights locally until
  the Transformers stack recognizes `gemma4`.
- Next proof should use either an official/source Transformers build with Gemma
  4 support, LiteRT-LM, or another supported runtime, followed by a short
  generation smoke and then the strict Hermes BFCL pilot.
