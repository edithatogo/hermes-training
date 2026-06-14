# Unsloth Qwen3.6 27B GGUF Acquisition Blocked - 2026-06-14

## Summary

`unsloth/Qwen3.6-27B-GGUF` was checked as priority 21 in the runtime-proof
action queue. This is the standard Unsloth GGUF packaging lane for Qwen3.6 27B.

The dry-run listed multiple GGUF artifacts. The smallest main model artifact
was:

- `Qwen3.6-27B-UD-IQ2_XXS.gguf`
- Reported size: `9.4G`

A live download of the smallest main artifact was started into the SSD-backed
Hugging Face cache. It made only partial progress during the bounded window and
was cancelled cleanly.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  unsloth/Qwen3.6-27B-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  unsloth/Qwen3.6-27B-GGUF \
  Qwen3.6-27B-UD-IQ2_XXS.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded.
- Live main-model download reached about `10M` and was cancelled.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--unsloth--Qwen3.6-27B-GGUF`
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry the main GGUF acquisition before any local endpoint proof.
- After acquisition, run strict BFCL endpoint scoring before promotion.
