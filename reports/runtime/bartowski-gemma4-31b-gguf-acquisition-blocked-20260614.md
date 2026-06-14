# Bartowski Gemma 4 31B GGUF Acquisition Blocked - 2026-06-14

## Summary

`bartowski/google_gemma-4-31B-it-GGUF` was checked as priority 17 in the
runtime-proof action queue. This is a community GGUF packaging lane for Gemma 4
31B instruct.

The dry-run listed many GGUF artifacts. The smallest main model artifact was:

- `google_gemma-4-31B-it-IQ1_M.gguf`
- Reported size: `10.1G`

Because this is an unusually small 31B quantization, it was not marked
size-blocked without attempting acquisition first.

A live download of the smallest main artifact was started into the SSD-backed
Hugging Face cache. It made only partial progress during the bounded window and
was cancelled cleanly.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  bartowski/google_gemma-4-31B-it-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  bartowski/google_gemma-4-31B-it-GGUF \
  google_gemma-4-31B-it-IQ1_M.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded.
- Live main-model download reached about `15M` and was cancelled.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--bartowski--google_gemma-4-31B-it-GGUF`
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry the main GGUF acquisition before any local endpoint proof.
- After acquisition, run a strict BFCL endpoint pilot before considering this
  31B low-bit lane useful.
