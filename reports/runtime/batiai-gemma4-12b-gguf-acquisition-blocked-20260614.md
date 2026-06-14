# Batiai Gemma 4 12B GGUF Acquisition Blocked - 2026-06-14

## Summary

`batiai/gemma-4-12B-it-GGUF` was checked as priority 12 in the runtime-proof
action queue. This is a community GGUF packaging lane for the Gemma 4 12B
instruct model.

The dry-run listed multiple GGUF artifacts. The smallest main model artifact
was:

- `google-gemma-4-12B-it-Q2_K_S.gguf`
- Reported size: `4.5G`

The repo also contains a `175.1M` mmproj file, but the main model artifact is
required before a local endpoint proof can be claimed.

A live download of `google-gemma-4-12B-it-Q2_K_S.gguf` was started into the
SSD-backed Hugging Face cache. It did not make useful progress during the
bounded window and was cancelled cleanly.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  batiai/gemma-4-12B-it-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  batiai/gemma-4-12B-it-GGUF \
  google-gemma-4-12B-it-Q2_K_S.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded.
- Live main-model download stalled at a zero-byte incomplete blob.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--batiai--gemma-4-12B-it-GGUF`
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry the main GGUF acquisition before any local endpoint proof.
- Keep this packaging lane behind strict BFCL endpoint scoring.
