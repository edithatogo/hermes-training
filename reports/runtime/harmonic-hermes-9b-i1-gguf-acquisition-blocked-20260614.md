# Harmonic-Hermes 9B i1 GGUF Acquisition Blocked - 2026-06-14

## Summary

`mradermacher/Harmonic-Hermes-9B-i1-GGUF` was checked as priority 6 in the
runtime-proof action queue. This is an alternative GGUF packaging lane for the
Harmonic-Hermes agentic fine-tune.

The dry-run listed several GGUF options. The smallest text-model artifact was:

- `Harmonic-Hermes-9B.i1-IQ1_S.gguf`
- Reported size: `2.7G`

A live download was started into the SSD-backed Hugging Face cache. The transfer
made partial progress, but only reached about `15M` after the first polling
window. It was cancelled cleanly because it would not complete in a reasonable
runtime-proof pass.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  mradermacher/Harmonic-Hermes-9B-i1-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  mradermacher/Harmonic-Hermes-9B-i1-GGUF \
  Harmonic-Hermes-9B.i1-IQ1_S.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded.
- Live download was cancelled after partial progress.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--mradermacher--Harmonic-Hermes-9B-i1-GGUF`
- Incomplete blob observed at about `15M`.
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry acquisition before any local endpoint proof.
- Keep this i1 packaging lane behind artifact acquisition, then strict BFCL
  endpoint scoring.
