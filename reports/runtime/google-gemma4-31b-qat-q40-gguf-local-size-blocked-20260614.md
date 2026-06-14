# Google Gemma 4 31B QAT q4_0 GGUF Local Size Blocked - 2026-06-14

## Summary

`google/gemma-4-31B-it-qat-q4_0-gguf` was checked as priority 19 in the
runtime-proof action queue. This is Google's QAT q4_0 GGUF packaging lane for
Gemma 4 31B instruct.

The dry-run listed:

- `gemma-4-31B_q4_0-it.gguf`: `17.7G`
- `gemma-4-31B-it-mmproj.gguf`: `1.2G`

The main model artifact is required before a local endpoint proof can be
claimed.

The smallest main artifact is too large for a bounded Mac-local proof on the
current 32GB lane. No live download was attempted.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  google/gemma-4-31B-it-qat-q4_0-gguf \
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
