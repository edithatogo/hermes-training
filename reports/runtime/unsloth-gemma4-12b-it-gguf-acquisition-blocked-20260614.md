# Unsloth Gemma 4 12B Instruct GGUF Acquisition Blocked - 2026-06-14

## Summary

`unsloth/gemma-4-12b-it-GGUF` was checked as priority 16 in the runtime-proof
action queue. This is the non-QAT Unsloth GGUF packaging lane for Gemma 4 12B
instruct.

The dry-run listed multiple GGUF artifacts. The smallest main model artifact
was:

- `gemma-4-12b-it-UD-IQ2_M.gguf`
- Reported size: `4.2G`

The repo also contains smaller MTP and mmproj files, but those do not substitute
for the main model artifact required by the Hermes endpoint proof.

A live download of the main artifact was started into the SSD-backed Hugging
Face cache. It made only partial progress during the bounded window and was
cancelled cleanly.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  unsloth/gemma-4-12b-it-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  unsloth/gemma-4-12b-it-GGUF \
  gemma-4-12b-it-UD-IQ2_M.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded.
- Live main-model download reached about `23M` and was cancelled.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--unsloth--gemma-4-12b-it-GGUF`
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry the main GGUF acquisition before any local endpoint proof.
- Keep MTP/mmproj-only work separate from the Hermes strict text/tool-call
  endpoint gate.
