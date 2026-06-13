# Specification: mem0 Queue Blocked Command Guard

## Overview

The mem0 candidate queue correctly marked some candidates as `access-gated` or
`runtime-blocked`, but the generated command cards still emitted runnable
benchmark commands. That made it easy to repeat known-failing work.

## Goals

- Keep blocked candidates visible in the queue.
- Replace runnable benchmark commands with fail-closed unblock notes for `access-gated` candidates.
- Replace runnable benchmark commands with fail-closed unblock notes for `runtime-blocked` candidates.
- Regenerate and validate the mem0 candidate queue.

## Acceptance Criteria

- `google/embeddinggemma-300m` no longer emits a sentence-transformers benchmark command while access-gated.
- `jinaai/jina-embeddings-v4` no longer emits a sentence-transformers benchmark command while runtime-blocked.
- Unit coverage locks both command guards.
- `scripts/validate_mem0_candidate_queue.py` and hub readiness validation pass.

## Out Of Scope

- Requesting gated model access.
- Upgrading Transformers or other shared dependencies.
- Running new mem0 benchmarks.
