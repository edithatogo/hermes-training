# MiniCPM-o 4.5 GGUF Acquisition Blocked - 2026-06-14

## Summary

`openbmb/MiniCPM-o-4_5-gguf` was checked as priority 10 in the runtime-proof
action queue. This is the GGUF packaging lane for the MiniCPM-o 4.5 multimodal
candidate.

The dry-run listed multiple GGUF artifacts. The smallest main text-model
artifacts were:

- `MiniCPM-o-4_5-Q4_0.gguf`
- `MiniCPM-o-4_5-Q4_K_S.gguf`
- Reported size: `4.8G`

The repo also contains smaller audio, TTS, token-to-wave, and vision components,
but those are not a substitute for the main text-model endpoint proof required
by the Hermes queue.

A live download of `MiniCPM-o-4_5-Q4_0.gguf` was started into the SSD-backed
Hugging Face cache. It made only partial progress during the bounded window and
was cancelled cleanly.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  openbmb/MiniCPM-o-4_5-gguf \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  openbmb/MiniCPM-o-4_5-gguf \
  MiniCPM-o-4_5-Q4_0.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded.
- Live text-model download reached about `16M` and was cancelled.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--openbmb--MiniCPM-o-4_5-gguf`
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry the main text GGUF acquisition before any local endpoint proof.
- Keep modality-component work separate from the Hermes strict text/tool-call
  endpoint gate.
