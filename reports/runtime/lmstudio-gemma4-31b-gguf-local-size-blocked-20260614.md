# LM Studio Gemma 4 31B GGUF Local Size Blocked - 2026-06-14

## Summary

`lmstudio-community/gemma-4-31B-it-GGUF` was checked as priority 20 in the
runtime-proof action queue. This is the LM Studio community GGUF packaging lane
for Gemma 4 31B instruct.

The dry-run listed:

- `gemma-4-31B-it-Q4_K_M.gguf`: `18.7G`
- `gemma-4-31B-it-Q6_K.gguf`: `25.2G`
- `gemma-4-31B-it-Q8_0.gguf`: `32.6G`
- `mmproj-gemma-4-31B-it-BF16.gguf`: `1.2G`

The main model artifact is required before a local endpoint proof can be
claimed.

The smallest main artifact is too large for a bounded Mac-local proof on the
current 32GB lane. No live download was attempted.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  lmstudio-community/gemma-4-31B-it-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

## Result

- Dry-run succeeded.
- No live download was attempted.
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `local-size-blocked`
- Use cloud/offload capacity or a smaller low-bit packaging lane before claiming
  local benchmark evidence.
