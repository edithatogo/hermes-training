# EmbeddingGemma Live mem0 Query-Guard Fixture Gate

## Overview

The replay gate showed that EmbeddingGemma's remaining mem0 miss could be fixed
by reranking, but replay evidence is not enough to promote a retrieval lane.
This track runs a fresh isolated mem0 add/search fixture with EmbeddingGemma
through a resilient llama.cpp embedding proxy and records the harness fixes
needed to avoid global mem0/Qdrant state collisions.

## Functional Requirements

- Run the live fixture without mutating the default `mem0_nomic_768`
  collection.
- Keep Qdrant state, history DB, server logs, and run summaries under
  `/Volumes/PortableSSD/hermes-evals`.
- Use an output-local `$HOME/.mem0` copy for mem0 subprocesses so Qdrant
  migration locks do not collide with the user's real mem0 store.
- Preserve access to the installed mem0 package and Homebrew dependencies via
  `PYTHONPATH`.
- Record a run card and update the mem0 benchmark summary.

## Non-Functional Requirements

- The fixture remains opt-in and does not change Hermes or mem0 defaults.
- The resilient proxy path is documented as runtime evidence, not as default
  integration.
- All server processes must stop after the run.

## Acceptance Criteria

- Fresh live fixture reaches top-1 `1.000` and recall@3 `1.000`.
- `query_terms_guarded` reaches top-1 `1.000` and recall@3 `1.000` within the
  same live run.
- `scripts/check_mem0_benchmark_evidence.py` passes.
- Focused mem0 tests and hub readiness pass.

## Out Of Scope

- Switching mem0 defaults from `nomic-embed-text:latest`.
- Migrating `mem0_nomic_768`.
- Creating a long-running embedding service.
