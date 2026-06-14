# AgentCPM Report GGUF Acquisition Blocked - 2026-06-14

## Summary

`openbmb/AgentCPM-Report-GGUF` was checked as priority 8 in the runtime-proof
action queue. This is the GGUF packaging lane for the AgentCPM deep research
agent candidate.

The dry-run listed one GGUF artifact:

- `AgentCPM-Report-Q4_K_M.gguf`
- Reported size: `5.0G`

A live download was started into the SSD-backed Hugging Face cache. It did not
make useful progress during the bounded window and was cancelled cleanly.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  openbmb/AgentCPM-Report-GGUF \
  --include '*.gguf' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  openbmb/AgentCPM-Report-GGUF \
  AgentCPM-Report-Q4_K_M.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded.
- Live download stalled at a zero-byte incomplete blob.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--openbmb--AgentCPM-Report-GGUF`
- No llama.cpp endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry artifact acquisition before any local endpoint proof.
- Keep this GGUF packaging lane behind strict BFCL endpoint scoring.
