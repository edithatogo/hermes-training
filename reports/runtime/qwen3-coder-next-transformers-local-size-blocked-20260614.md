# Qwen3 Coder Next Transformers Local Size Blocked - 2026-06-14

## Summary

`Qwen/Qwen3-Coder-Next` was checked as priority 25 in the runtime-proof action
queue. This is the source Transformers model for the subquadratic Qwen coding
agent family.

The dry-run listed 40 safetensor shards:

- 39 shards at `4.0G`
- 1 shard at `3.4G`
- Total before runtime overhead: about `159.4G`

This is not a Mac-local Transformers proof lane on the current 32GB machine.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  Qwen/Qwen3-Coder-Next \
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
- Use cloud/specialist runtime proof for the source model.
- Use the GGUF tree for local Hermes-agent smoke work.
