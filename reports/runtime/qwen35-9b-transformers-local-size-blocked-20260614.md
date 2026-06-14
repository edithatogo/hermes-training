# Qwen3.5 9B Transformers Local Size Blocked - 2026-06-14

## Summary

`Qwen/Qwen3.5-9B` was checked as priority 5 in the runtime-proof action queue.
The model is not present in the SSD-backed Hugging Face cache.

A dry-run download showed four safetensor shards totaling about `19.3G` before
runtime overhead. On the current 32 GB Apple Silicon local lane, that is too
large for a responsible first direct Transformers BFCL proof.

## Command

```bash
/Users/doughnut/.local/bin/hf download \
  Qwen/Qwen3.5-9B \
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
- Prefer smaller Qwen helper lanes, quantized GGUF/MLX packaging, or a cloud
  runtime proof once capacity and cost gates are open.
