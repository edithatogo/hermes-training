# EmbeddingGemma mem0 Default Integration Gate

## Overview

EmbeddingGemma now has live isolated mem0 fixture evidence through a resilient
llama.cpp embedding proxy, with raw vector and query-guarded strategies reaching
top-1 `1.000` and recall@3 `1.000`. That proof is intentionally non-default.
This track turns the proof into a promotion-ready integration lane by defining
how EmbeddingGemma can be launched, selected, rolled back, and compared against
the current `nomic-embed-text:latest` / `mem0_nomic_768` default without
mutating the user's live store by accident.

## Functional Requirements

- Add an opt-in mem0 embedding runtime profile for EmbeddingGemma over the
  resilient llama.cpp proxy.
- Keep the current nomic default as the default unless a final promotion commit
  explicitly changes it.
- Provide a documented rollback path that returns reads and writes to
  `nomic-embed-text:latest` and `mem0_nomic_768`.
- Decide and document collection strategy:
  - reuse only if the embedding dimensions and distance metric are compatible;
  - otherwise create a new named collection and require explicit migration.
- Add a bounded smoke command that proves add/search through the opt-in profile
  with SSD-local logs and Qdrant state.
- Record evidence in mem0 run cards, `MODEL_CANDIDATES.yaml`,
  `FUTURE_MODELS.md`, and the mem0 benchmark index.

## Non-Functional Requirements

- No benchmark or fixture output may write outside `/Volumes/PortableSSD`.
- The integration must stop server processes reliably after smoke tests.
- The profile must support llama.cpp directly and remain compatible with LM
  Studio or Ollama-style OpenAI-compatible embedding endpoints where possible.
- Promotion language must distinguish runtime proof, opt-in profile readiness,
  and default mem0 switch readiness.

## Acceptance Criteria

- Opt-in EmbeddingGemma mem0 profile can be launched reproducibly from tracked
  commands.
- Rollback command and default profile are documented and tested at least by
  config inspection or a small smoke.
- Collection compatibility decision is documented with the current 768-dim
  result and a clear migration rule.
- Focused mem0 tests, mem0 evidence validation, model-candidate validation, and
  hub readiness pass.
- `conductor/tracks.md` accurately reflects the track status.

## Out Of Scope

- Publishing new model artifacts.
- Migrating the user's real mem0 history automatically.
- Changing Hermes-agent to call mem0 on every turn.
- Replacing all reranking strategies with `query_terms_guarded`.
