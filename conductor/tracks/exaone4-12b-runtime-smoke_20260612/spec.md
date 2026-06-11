# Spec: EXAONE 4.0 1.2B Runtime Smoke

## Problem

EXAONE 4.0 1.2B was listed as a small local candidate but had no local runtime
evidence. The MLX 4-bit package is the preferred Mac path, with official GGUF
as a fallback runtime proof.

## Scope

- Verify EXAONE 4.0 1.2B MLX/GGUF package availability.
- Acquire the MLX 4-bit package to SSD and attempt the direct MLX smoke.
- Acquire the official Q4_K_M GGUF to SSD and run bounded llama.cpp generation.
- Record the MLX blocker and GGUF output behavior.
- Update model radar, proof queue, handoff, and Conductor registry.

## Out Of Scope

- No fine-tuning.
- No BFCL/local pilot run through GGUF.
- No endpoint wrapping or publication.

## Acceptance Criteria

- Artifact paths are SSD-backed.
- MLX failure is captured with concrete error text.
- GGUF runtime proof records command, timing, memory, and output blocker.
- Full validation passes.
