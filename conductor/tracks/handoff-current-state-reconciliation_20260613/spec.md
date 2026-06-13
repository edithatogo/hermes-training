# Spec

## Problem

`HANDOFF.md` is the operator pickup document for this project, but it still
carried 2026-06-12 state after the 2026-06-13 EmbeddingGemma, MLX BGE, and
submodule-push work. That creates a risk that the next agent follows stale
hashes or repeats completed mem0 latency gates.

## Scope

- Update the handoff date and submodule pointers.
- Record the current EmbeddingGemma and MLX BGE mem0 decisions.
- Remove stale wording that says the broader MLX BGE cold/warm probe is still
  pending.
- Keep this to documentation/state reconciliation only.

## Non-Goals

- Running new model benchmarks.
- Changing mem0, Hermes, or model defaults.
- Publishing Hugging Face artifacts.

## Acceptance

- `HANDOFF.md` reflects the current pushed hub and submodule state.
- The MLX BGE next action no longer asks for the completed broader cold/warm
  probe.
- Conductor metadata and track registry are consistent.
- Readiness validation passes before push.
