# DuoNeural OpenYourMind Gemma4 12B GGUF Acquisition Blocked - 2026-06-14

## Summary

`DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF` was checked as
priority 11 in the runtime-proof action queue. This is a community GGUF
packaging lane for the OpenYourMind abliterated Gemma 4 12B instruct model.

The dry-run listed four GGUF artifacts. The smallest artifact was:

- `oym_ablit-Q3_K_L.gguf`
- Reported size: `6.6G`

A live download was started into the SSD-backed Hugging Face cache. It made only
minimal progress during the bounded window and was cancelled cleanly.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF \
  oym_ablit-Q3_K_L.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded.
- Live download reached about `5.1M` and was cancelled.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--DuoNeural--OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF`
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry artifact acquisition before any local endpoint proof.
- Keep this GGUF packaging lane behind strict BFCL endpoint scoring.
