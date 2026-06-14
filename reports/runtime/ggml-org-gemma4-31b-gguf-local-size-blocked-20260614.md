# ggml-org Gemma 4 31B GGUF Local Size Blocked - 2026-06-14

## Summary

`ggml-org/gemma-4-31B-it-GGUF` was checked as priority 18 in the runtime-proof
action queue. This is a ggml-org GGUF packaging lane for Gemma 4 31B instruct.

The dry-run listed three main model artifacts:

- `gemma-4-31B-it-Q4_K_M.gguf`: `18.7G`
- `gemma-4-31B-it-Q8_0.gguf`: `32.6G`
- `gemma-4-31B-it-bf16.gguf`: `61.4G`

The repo also contains mmproj files, but the main model artifact is required for
the Hermes endpoint proof.

The smallest main artifact is too large for a bounded Mac-local proof on the
current 32GB lane. No live download was attempted, especially after the smaller
10.1G Bartowski 31B artifact made only partial progress during its bounded
acquisition attempt.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  ggml-org/gemma-4-31B-it-GGUF \
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
