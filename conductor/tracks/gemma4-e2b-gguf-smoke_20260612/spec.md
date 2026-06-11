# Spec: Gemma 4 E2B QAT GGUF Runtime Smoke

## Problem

The current Gemma 4 lane listed E4B/12B QAT as next runtime candidates, but the
repo had no fresh official Gemma 4 small-model runtime proof. The safest first
step was the official E2B QAT q4_0 text GGUF, which is small enough for the
MacBook Pro M1 Max and SSD cache.

## Scope

- Verify current Gemma 4 E2B/E4B/12B QAT package availability.
- Acquire only the E2B text GGUF to `/Volumes/PortableSSD/huggingface/hub`.
- Run a bounded `llama-completion` text smoke.
- Record runtime warnings and empty-output blocker.
- Update radar, queue, handoff, and track registry.

## Out Of Scope

- No multimodal projector download.
- No E4B/12B acquisition in this slice.
- No fine-tuning, BFCL claim, or publication.

## Acceptance Criteria

- The artifact is SSD-backed.
- The smoke command is bounded and exits cleanly.
- Empty-output behavior is fail-closed and documented.
- Project validations pass.
