# Gemma 4 12B Instruct Transformers Local Size Blocked - 2026-06-14

## Summary

`google/gemma-4-12B-it` was checked as priority 14 in the runtime-proof action
queue. This is the instruct Gemma 4 12B Transformers lane.

The dry-run listed one safetensors artifact:

- `model.safetensors`
- Reported size: `23.9G`

On the current MacBook Pro M1 Max 32GB lane, downloading and loading this full
Transformers artifact is not a bounded local proof path.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  google/gemma-4-12B-it \
  --include '*.safetensors' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

## Result

- Dry-run succeeded.
- No live download was attempted.
- No Transformers pilot was run.

## Decision

- Status: `local-size-blocked`
- Use a quantized packaging lane or cloud/offloaded runtime proof before any
  benchmark claim.
