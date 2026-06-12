# North-Mini-Code GGUF Packaging Refresh - 2026-06-12

## Summary

This refresh captures the new `unsloth/North-Mini-Code-1.0-GGUF` packaging lane
that surfaced in the live Hugging Face search. It is useful as a code-agent
comparison point for Hermes workflows, but the local runtime remains blocked
until `cohere2moe` is supported by the executor.

## Verified Open-Weight Candidates

| Family | Verified release | Why it matters |
|---|---|---|
| Cohere | `unsloth/North-Mini-Code-1.0-GGUF` | Fresh GGUF packaging published today for the 30B total / 3B active code-specialist model. Good as packaging evidence and as a future runtime candidate once the backend supports `cohere2moe`. |

## Watchlist Status

- The packaging lane is source-backed and ready for future runtime proof.
- The current local runtime is still blocked by missing `cohere2moe` support.
- Do not spin up a new local smoke loop against the same llama.cpp build until
  the executor changes.

## Decision

- Add `unsloth/North-Mini-Code-1.0-GGUF` to the machine-readable radar.
- Keep the lane marked `runtime-blocked` until the backend can load `cohere2moe`.
- Treat the new packaging as a Hermes agent comparison lane, not as a current training target.
