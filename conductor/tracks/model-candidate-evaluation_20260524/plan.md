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
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Candidate Matrix And Shared Gates' (Protocol in workflow.md)

## Phase 2 - Lane A Mac-Local Candidates

- [x] Task: Inventory Mac-local candidate classes without downloading models.
    - [x] Capture MLX-compatible candidates.
    - [x] Capture Ollama and LM Studio candidates.
    - [x] Capture GGUF fallback candidates.
- [x] Task: Define Mac-local evaluation dimensions.
    - [x] Memory fit on M1 Max 32GB unified memory.
    - [x] Runtime endpoint compatibility.
    - [x] Context length and prompt-format behavior.
    - [x] Tool-call strictness and normalization requirements.
    - [x] Adapter-training feasibility.
- [x] Task: Define Mac-local evidence requirements.
    - [x] Runtime smoke evidence before benchmark claims.
    - [x] Raw and normalized output samples when wrappers or formatting repairs are involved.
    - [x] SSD-backed artifact paths for any future runs.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Lane A Mac-Local Candidates' (Protocol in workflow.md)

## Phase 3 - Lane B Hermes 4 And Qwen3.6 Teacher Baselines

- [x] Task: Define teacher-baseline roles.
    - [x] Answer-quality comparison.
    - [x] Tool-call repair target.
    - [x] Dataset critique and filtering.
    - [x] Benchmark normalization reference.
- [x] Task: Define teacher-baseline evidence requirements.
    - [x] Record model family, version, endpoint or runtime, license/terms, cost assumptions, and reproducibility notes.
    - [x] Separate teacher output evidence from student benchmark evidence.
    - [x] Require prompt and sampling settings for any future teacher run.
- [x] Task: Define teacher-baseline stop conditions.
    - [x] Stop if access requires unavailable credentials or license acceptance.
    - [x] Stop if cost or quota guardrails are unknown.
    - [x] Stop if teacher output would be used as publish evidence without benchmark corroboration.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Lane B Hermes 4 And Qwen3.6 Teacher Baselines' (Protocol in workflow.md)

## Phase 4 - Lane C Retrieval And Embedding Candidates

- [x] Task: Define retrieval candidate categories.
    - [x] Embedding models.
    - [x] Rerankers.
    - [x] Sparse or hybrid retrieval components.
    - [x] Hermes memory/RAG integration candidates.
- [x] Task: Define retrieval-specific gates.
    - [x] Retrieval quality and recall.
    - [x] Reranking quality.
    - [x] Latency and storage footprint.
    - [x] RAG answer grounding and citation behavior.
    - [x] MTEB-style or project-local retrieval evidence.
- [x] Task: Define boundary with chat-model evaluation.
    - [x] Retrieval wins do not imply chat SFT wins.
    - [x] Chat-model wins do not imply embedding or retrieval wins.
    - [x] Combined RAG promotion requires both retrieval and answer-quality evidence.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Lane C Retrieval And Embedding Candidates' (Protocol in workflow.md)

## Phase 5 - Lane D Research Runtimes

- [x] Task: Define research-runtime categories.
    - [x] Subquadratic and Mamba-family runtimes.
    - [x] Recurrent and RWKV-family runtimes.
    - [x] BitNet candidates.
    - [x] KTransformers-style or other specialist serving paths.
- [x] Task: Define runtime-proof requirements.
    - [x] Verified weights and license.
    - [x] Reproducible setup path.
    - [x] Endpoint or invocation contract.
    - [x] Prompt-format compatibility.
    - [x] Benchmark comparability limits.
- [x] Task: Define promotion and watchlist rules.
    - [x] Promote only when runtime proof is reproducible.
    - [x] Keep immature runtimes on watchlist with concrete blockers.
    - [x] Avoid presenting research-runtime success as Hermes product readiness without agent benchmarks.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 5 - Lane D Research Runtimes' (Protocol in workflow.md)

## Phase 6 - Lane E Publish / No-Publish Decisions And Synthesis

- [x] Task: Create the decision rubric.
    - [x] Reject.
    - [x] Watchlist.
    - [x] Runtime-proof only.
    - [x] Benchmark candidate.
    - [x] Internal adapter candidate.
    - [x] Publish candidate.
- [x] Task: Define final synthesis report structure.
    - [x] Candidate matrix summary.
    - [x] Lane winners and rejected candidates.
    - [x] Evidence links and gaps.
    - [x] Required follow-up tracks.
    - [x] Explicit publish/no-publish decisions.
- [x] Task: Validate setup-only scope.
    - [x] Confirm no large model downloads were performed.
    - [x] Confirm no benchmark artifacts were generated.
    - [x] Confirm future artifact paths remain SSD-backed.
    - [x] Run hub readiness validation if code or docs outside this track changed.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 6 - Lane E Publish / No-Publish Decisions And Synthesis' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: `reports/model-radar/candidate-matrix-20260524.md` records candidate states and next actions. `reports/model-radar/candidate-selection-synthesis-20260524.md` records lane winners, no-publish decisions, evidence links, and next parallel work. The track remains setup/readiness only; live runtime proofs and benchmarks are handled by separate execution tracks.
