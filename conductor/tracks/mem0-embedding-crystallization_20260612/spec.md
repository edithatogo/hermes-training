# Specification: mem0 and Embedding Crystallization

## Overview

The mem0 lane needs a stable model map so the repo can keep iterating on
embeddings, rerankers, and helper flows without mutating the live mem0
configuration.

This track makes the mem0 queue explicit for:

- the current default embedding path
- alternate embeddings that can replace or compete with nomic
- rerankers and retrieval helpers used by mem0
- models that are useful for Hermes memory workflows but not mem0 defaults

## Scope

- Align mem0-related tracks with the current embedding shortlist.
- Update `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, and `HANDOFF.md` so the
  mem0 queue is clear.
- Keep the live mem0 configuration untouched in this slice.
- Preserve the distinction between embeddings, rerankers, and chat models.

## Out Of Scope

- No live mem0 config mutation.
- No benchmarking publication claims.
- No training runs in this slice.

## Acceptance Criteria

- The mem0 shortlist is explicit and stable.
- The repo distinguishes the current default embedding from alternate
  candidates.
- Embedding candidates are grouped by role and runtime fit rather than by
  marketing name alone.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.5 / 10`
- Evidence: the work is a bounded documentation and candidate-classification
  slice with clear non-goals.
- Remaining gap: runtime proof and benchmark work still need follow-on tracks.
