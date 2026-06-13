# EmbeddingGemma mem0 Query-Guard Replay Gate

## Overview

EmbeddingGemma GGUF now passes the isolated embedding differentiation suite,
but its live mem0 fixture still has one top-1 miss where the correct answer is
inside the top three and the vector top result is a negated runtime-boundary
distractor. This track adds a read-only replay gate and a query-aware guarded
reranker to determine whether the remaining miss is an embedding-recall issue
or a reranking-policy issue.

## Functional Requirements

- Add a `query_terms_guarded` reranker strategy that can penalize negated
  runtime/path memories when the query asks for validated paths.
- Pass the query text through fixed-suite, mem0 search, and isolated-fixture
  reranking paths when the guarded strategy is selected.
- Rebuild replay candidates from captured live fixture `results.jsonl`
  evidence without mutating mem0 collections.
- Generate run cards and index entries for both vector replay and guarded replay.
- Update the model radar and future-model notes to reflect EmbeddingGemma GGUF
  as a benchmarked, non-default Mac-local challenger.

## Non-Functional Requirements

- Replay outputs remain under `/Volumes/PortableSSD/hermes-evals`.
- The guarded reranker is opt-in and must not change the live mem0 default.
- The evidence must distinguish replay proof from live fixture promotion.
- Unit tests cover the negated runtime/path penalty and run-card command shape.

## Acceptance Criteria

- Vector replay reproduces the live miss at top-1 `0.909`.
- `query_terms_guarded` replay reaches top-1 `1.000` and recall@3 `1.000`.
- `scripts/check_mem0_benchmark_evidence.py` passes.
- `scripts/check_mem0_model_candidates.py` passes.
- Focused unit tests and hub readiness pass.

## Out Of Scope

- Promoting EmbeddingGemma as the mem0 default.
- Running a fresh live guarded fixture as part of this replay-only track.
- Changing Hermes runtime defaults.
