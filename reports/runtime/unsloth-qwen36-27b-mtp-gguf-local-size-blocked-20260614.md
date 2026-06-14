# Unsloth Qwen3.6 27B MTP GGUF Local Size Blocked - 2026-06-14

## Summary

`unsloth/Qwen3.6-27B-MTP-GGUF` was checked as priority 22 in the runtime-proof
action queue. This is the multi-token prediction GGUF packaging lane for
Qwen3.6 27B.

The dry-run listed multiple GGUF artifacts. The smallest main model artifact
was:

- `Qwen3.6-27B-UD-IQ2_XXS.gguf`
- Reported size: `9.6G`

The sibling non-MTP Qwen3.6 27B GGUF repo has a similar `9.4G` smallest main
artifact and made only partial progress in a bounded acquisition attempt. This
MTP lane is therefore not a distinct smaller local proof path.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  unsloth/Qwen3.6-27B-MTP-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

## Result

- Dry-run succeeded.
- No live download was attempted for the MTP sibling.
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `local-size-blocked`
- Use cloud/offload capacity or a smaller low-bit packaging lane before claiming
  local benchmark evidence.
