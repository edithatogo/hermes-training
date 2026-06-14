# Unsloth Gemma 4 31B GGUF Acquisition Blocked - 2026-06-14

## Summary

`unsloth/gemma-4-31B-it-GGUF` was checked as priority 24 in the runtime-proof
action queue. This is the Unsloth GGUF packaging lane for Gemma 4 31B instruct.

The dry-run listed multiple GGUF artifacts. The smallest main model artifact
was:

- `gemma-4-31B-it-UD-IQ2_XXS.gguf`
- Reported size: `8.5G`

A live download of the smallest main artifact was started into the SSD-backed
Hugging Face cache. It made only partial progress during the bounded window and
was cancelled cleanly.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  unsloth/gemma-4-31B-it-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  unsloth/gemma-4-31B-it-GGUF \
  gemma-4-31B-it-UD-IQ2_XXS.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded.
- Live main-model download reached about `15M` and was cancelled.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--unsloth--gemma-4-31B-it-GGUF`
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry the main GGUF acquisition before any local endpoint proof.
- After acquisition, run strict BFCL endpoint scoring before promotion.
