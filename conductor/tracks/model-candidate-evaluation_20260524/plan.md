# Plan: Model Candidate Evaluation And Selection

## Phase 1 - Candidate Matrix And Shared Gates

- [x] Task: Define the candidate matrix schema.
    - [x] Include model/runtime name, lane, source, version, license, serving mode, memory estimate, context length, tool-call notes, embedding/retrieval notes, storage root, decision state, evidence links, and blockers.
    - [x] Keep the template lightweight enough to live in Markdown or CSV without requiring benchmark artifacts.
- [x] Task: Define common promotion gates.
    - [x] Watchlist to runtime proof: source, license, weights or endpoint, runtime path, and SSD storage plan are known.
    - [x] Runtime proof to benchmark candidate: endpoint behavior, prompt format, context behavior, and artifact paths are reproducible.
    - [x] Benchmark candidate to publish candidate: benchmark evidence, license, model card, artifact review, and explicit approval are complete.
- [x] Task: Define no-publish gates.
    - [x] Block publication for missing or incompatible license evidence.
    - [x] Block publication for unnormalized or non-reproducible benchmarks.
    - [x] Block publication for failed Hermes tool-call gates when the candidate is presented as an agent model.
    - [x] Block publication when artifacts or caches are outside SSD-backed roots.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Candidate Matrix And Shared Gates' (Protocol in workflow.md)

## Phase 2 - Lane A Mac-Local Candidates

- [ ] Task: Inventory Mac-local candidate classes without downloading models.
    - [ ] Capture MLX-compatible candidates.
    - [ ] Capture Ollama and LM Studio candidates.
    - [ ] Capture GGUF fallback candidates.
- [ ] Task: Define Mac-local evaluation dimensions.
    - [ ] Memory fit on M1 Max 32GB unified memory.
    - [ ] Runtime endpoint compatibility.
    - [ ] Context length and prompt-format behavior.
    - [ ] Tool-call strictness and normalization requirements.
    - [ ] Adapter-training feasibility.
- [ ] Task: Define Mac-local evidence requirements.
    - [ ] Runtime smoke evidence before benchmark claims.
    - [ ] Raw and normalized output samples when wrappers or formatting repairs are involved.
    - [ ] SSD-backed artifact paths for any future runs.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Lane A Mac-Local Candidates' (Protocol in workflow.md)

## Phase 3 - Lane B Hermes 4 And Qwen3.6 Teacher Baselines

- [ ] Task: Define teacher-baseline roles.
    - [ ] Answer-quality comparison.
    - [ ] Tool-call repair target.
    - [ ] Dataset critique and filtering.
    - [ ] Benchmark normalization reference.
- [ ] Task: Define teacher-baseline evidence requirements.
    - [ ] Record model family, version, endpoint or runtime, license/terms, cost assumptions, and reproducibility notes.
    - [ ] Separate teacher output evidence from student benchmark evidence.
    - [ ] Require prompt and sampling settings for any future teacher run.
- [ ] Task: Define teacher-baseline stop conditions.
    - [ ] Stop if access requires unavailable credentials or license acceptance.
    - [ ] Stop if cost or quota guardrails are unknown.
    - [ ] Stop if teacher output would be used as publish evidence without benchmark corroboration.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Lane B Hermes 4 And Qwen3.6 Teacher Baselines' (Protocol in workflow.md)

## Phase 4 - Lane C Retrieval And Embedding Candidates

- [ ] Task: Define retrieval candidate categories.
    - [ ] Embedding models.
    - [ ] Rerankers.
    - [ ] Sparse or hybrid retrieval components.
    - [ ] Hermes memory/RAG integration candidates.
- [ ] Task: Define retrieval-specific gates.
    - [ ] Retrieval quality and recall.
    - [ ] Reranking quality.
    - [ ] Latency and storage footprint.
    - [ ] RAG answer grounding and citation behavior.
    - [ ] MTEB-style or project-local retrieval evidence.
- [ ] Task: Define boundary with chat-model evaluation.
    - [ ] Retrieval wins do not imply chat SFT wins.
    - [ ] Chat-model wins do not imply embedding or retrieval wins.
    - [ ] Combined RAG promotion requires both retrieval and answer-quality evidence.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Lane C Retrieval And Embedding Candidates' (Protocol in workflow.md)

## Phase 5 - Lane D Research Runtimes

- [ ] Task: Define research-runtime categories.
    - [ ] Subquadratic and Mamba-family runtimes.
    - [ ] Recurrent and RWKV-family runtimes.
    - [ ] BitNet candidates.
    - [ ] KTransformers-style or other specialist serving paths.
- [ ] Task: Define runtime-proof requirements.
    - [ ] Verified weights and license.
    - [ ] Reproducible setup path.
    - [ ] Endpoint or invocation contract.
    - [ ] Prompt-format compatibility.
    - [ ] Benchmark comparability limits.
- [ ] Task: Define promotion and watchlist rules.
    - [ ] Promote only when runtime proof is reproducible.
    - [ ] Keep immature runtimes on watchlist with concrete blockers.
    - [ ] Avoid presenting research-runtime success as Hermes product readiness without agent benchmarks.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 5 - Lane D Research Runtimes' (Protocol in workflow.md)

## Phase 6 - Lane E Publish / No-Publish Decisions And Synthesis

- [ ] Task: Create the decision rubric.
    - [ ] Reject.
    - [ ] Watchlist.
    - [ ] Runtime-proof only.
    - [ ] Benchmark candidate.
    - [ ] Internal adapter candidate.
    - [ ] Publish candidate.
- [ ] Task: Define final synthesis report structure.
    - [ ] Candidate matrix summary.
    - [ ] Lane winners and rejected candidates.
    - [ ] Evidence links and gaps.
    - [ ] Required follow-up tracks.
    - [ ] Explicit publish/no-publish decisions.
- [ ] Task: Validate setup-only scope.
    - [ ] Confirm no large model downloads were performed.
    - [ ] Confirm no benchmark artifacts were generated.
    - [ ] Confirm future artifact paths remain SSD-backed.
    - [ ] Run hub readiness validation if code or docs outside this track changed.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 6 - Lane E Publish / No-Publish Decisions And Synthesis' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.1 / 10
- Evidence: `reports/model-radar/candidate-matrix-20260524.md` now records candidate states and next actions. Health remains below completion threshold until lane-specific runtime evidence and final synthesis are complete.
