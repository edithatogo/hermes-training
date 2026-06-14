# Unsloth Qwen3.6 27B MLX Local Size Blocked - 2026-06-14

## Summary

`unsloth/Qwen3.6-27B-UD-MLX-4bit` was checked as priority 23 in the
runtime-proof action queue. This is the MLX 4-bit packaging lane for Qwen3.6
27B.

The dry-run listed five safetensor shards:

- Four shards at `5.4G`
- One shard at `4.7G`
- Total before runtime overhead: about `25.8G`

MLX is installed in the Hermes environment, but this artifact is too large for a
bounded proof on the current 32GB Mac-local lane.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  unsloth/Qwen3.6-27B-UD-MLX-4bit \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

## Result

- Dry-run succeeded.
- No live download was attempted.
- No MLX endpoint pilot was run.

## Decision

- Status: `local-size-blocked`
- Use cloud/offload capacity or a smaller MLX artifact before claiming local
  benchmark evidence.
