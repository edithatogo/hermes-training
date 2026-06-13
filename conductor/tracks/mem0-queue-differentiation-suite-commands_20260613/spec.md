# Specification: mem0 Queue Differentiation Suite Commands

## Overview

The mem0 candidate queue already records broader differentiation-suite evidence
for several embedding candidates. Some generated command cards still pointed at
the smaller `memory_retrieval_suite.json`, which could accidentally rerun a
weaker gate when the candidate status called for broader comparison.

## Goals

- Select the embedding benchmark suite from the candidate `first_gate` and status.
- Use `memory_retrieval_differentiation_suite.json` for differentiation-suite and benchmarked embedding candidates.
- Keep the smaller retrieval suite for baseline smoke/rollback candidates.
- Regenerate and validate the mem0 candidate queue.

## Acceptance Criteria

- BGE-M3 benchmarked command cards use the differentiation suite.
- Jina v5 omni text-matching MLX differentiation command cards use the differentiation suite.
- Unit coverage locks the suite selection behavior.
- `scripts/validate_mem0_candidate_queue.py` and hub readiness validation pass.

## Out Of Scope

- Running new mem0 benchmarks.
- Changing mem0 defaults.
- Changing candidate promotion status.
