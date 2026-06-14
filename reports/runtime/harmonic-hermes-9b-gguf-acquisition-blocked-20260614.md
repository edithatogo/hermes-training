# Harmonic-Hermes 9B GGUF Acquisition Blocked - 2026-06-14

## Summary

`DJLougen/Harmonic-Hermes-9B-GGUF` was checked as priority 4 in the
runtime-proof action queue. This is the preferred local route for the Harmonic
family after the full `DJLougen/Harmonic-9B` safetensors package proved too
large for a first Mac-local Transformers proof.

The dry-run listed several GGUF options. The smallest text-model artifact was:

- `Harmonic-Hermes-9B-Q2_K.gguf`
- Reported size: `3.8G`

A live download was started into the SSD-backed Hugging Face cache. Unlike the
previous Unsloth transfer, this download did make progress, but only reached
about `36M` after several polling windows. It was cancelled cleanly because it
would not complete in a reasonable runtime-proof pass.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  DJLougen/Harmonic-Hermes-9B-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  DJLougen/Harmonic-Hermes-9B-GGUF \
  Harmonic-Hermes-9B-Q2_K.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded.
- Live download was cancelled after partial progress.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--DJLougen--Harmonic-Hermes-9B-GGUF`
- Incomplete blob observed at about `36M`.
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry acquisition before any local endpoint proof.
- Keep the full Harmonic family behind artifact acquisition, then strict BFCL
  endpoint scoring.
