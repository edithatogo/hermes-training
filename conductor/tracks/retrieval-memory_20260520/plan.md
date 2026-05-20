# Plan: Retrieval and Hermes Memory Model Lane

## Phase 1 — Lane Definition

- [x] Add retrieval role/environment to model radar.
- [x] Add BGE-M3 and Jina candidates.
- [x] Add Qwen embedding/reranker candidates after model-card verification.
- [x] Update benchmark docs with retrieval-specific gates.

## Phase 2 — Dataset And Evaluation

- [x] Define Hermes memory/RAG eval scenarios.
- [x] Add contrastive JSONL contract for anchor/positive/negative examples.
- [x] Add MTEB or retrieval benchmark command shape.

## Phase 3 — Runtime Integration

- [x] Decide local vector store and retriever serving shape.
- [x] Add Hermes integration contract for retrieval calls.
- [x] Add publication docs for retriever cards.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: lane contracts, benchmark commands, serving shape, publication rules, and verified Qwen embedding/reranker candidates are documented.
- Gaps: future implementation wiring remains outside this planning/docs lane.
- Decision: complete for the Conductor lane setup.
