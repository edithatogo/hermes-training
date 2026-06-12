# Plan: mem0 and Embedding Crystallization

## Phase 1: mem0 Queue Audit

- [x] Task: inventory the existing mem0 tracks, the current default embedder, and the current reranker path.
- [x] Task: classify embeddings and rerankers into default, alternate, helper, and benchmark-only lanes.
- [x] Task: record where the mem0 queue still depends on nomic or other legacy assumptions.
- [x] Task: Conductor - Automated Review and Checkpoint 'mem0 Queue Audit' (Protocol in workflow.md)

## Phase 2: Candidate and Doc Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the mem0 embedding and reranker lane decisions.
- [x] Task: update `FUTURE_MODELS.md` and `HANDOFF.md` with the crystallized mem0 queue.
- [x] Task: keep the live mem0 configuration unchanged and document that boundary.
- [x] Task: Conductor - Automated Review and Checkpoint 'Candidate and Doc Sync' (Protocol in workflow.md)

## Phase 3: Validation

- [x] Task: run candidate validation and markdown/repo sanity checks.
- [x] Task: capture the final mem0 shortlist state and any follow-on proof items.
- [x] Task: Conductor - Automated Review and Checkpoint 'Validation' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.5 / 10
- Evidence: this slice preserves mem0 stability while making the embedding
  roadmap explicit.
- Gaps: runtime proof and live mem0 integration remain separate work.
