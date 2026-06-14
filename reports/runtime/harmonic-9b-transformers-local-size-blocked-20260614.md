# Harmonic 9B Transformers Local Size Blocked - 2026-06-14

## Summary

`DJLougen/Harmonic-9B` was checked as priority 3 in the runtime-proof action
queue. The package is a full Transformers/safetensors backbone for the
Harmonic-Hermes family, not a quantized Mac-local GGUF artifact.

The model is not present in the SSD-backed Hugging Face cache. A dry-run
download showed four safetensor shards totaling about `19.3G` before activation
memory, tokenizer/runtime overhead, and benchmark context. On the current 32 GB
Apple Silicon local lane, that is not a safe first proof target for a direct
Transformers BFCL pilot.

## Command

```bash
/Users/doughnut/.local/bin/hf download \
  DJLougen/Harmonic-9B \
  --include '*.safetensors' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

## Dry-Run Result

```text
model.safetensors-00001-of-00004.safetensors  5.3G
model.safetensors-00002-of-00004.safetensors  5.3G
model.safetensors-00003-of-00004.safetensors  5.4G
model.safetensors-00004-of-00004.safetensors  3.3G
```

## Decision

- Status: `local-size-blocked`
- Do not acquire the full safetensors package for the Mac-local proof lane yet.
- Route local testing through the Harmonic-Hermes GGUF packages first.
- Revisit this candidate as a cloud-teacher/runtime proof if GPU capacity and
  cost gates are open.
