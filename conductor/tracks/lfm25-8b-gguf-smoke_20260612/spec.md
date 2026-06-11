# Spec: LFM2.5 8B A1B GGUF Runtime Smoke

## Problem

The model radar identified `LiquidAI/LFM2.5-8B-A1B` as a newer LFM candidate,
but the repo had no local runtime proof for the 8B LFM2.5 artifact. Without a
bounded smoke, the project could not distinguish a viable Mac comparison
baseline from a speculative candidate.

## Scope

- Verify the official Hugging Face repo and Q4_K_M GGUF file.
- Acquire the artifact into `/Volumes/PortableSSD/huggingface/hub`.
- Run a bounded llama.cpp generation smoke.
- Record load/generation behavior and any Hermes prompt-compliance blocker.
- Update the model candidate radar and runtime proof queue.

## Out Of Scope

- No fine-tuning.
- No BFCL, lm-eval, or broad benchmark claim.
- No publication or default runtime change.

## Acceptance Criteria

- Artifact path is SSD-backed.
- The smoke command has a hard timeout and exits without leaving a process.
- Runtime status is recorded as pass/fail with exact blocker.
- Project validations pass.
