# Plan: Runtime Packaging and Hermes Validation

## Phase 1: MLX Runtime

- [x] Task: Validate adapter loading through MLX generation.
- [x] Task: Document MLX server command and endpoint.
- [x] Task: Conductor - Automated Review and Checkpoint 'MLX Runtime' (Protocol in workflow.md)

## Phase 2: Ollama/LM Studio

- [ ] Task: Validate Modelfiles and Ollama runtime smoke where model format supports it.
- [x] Task: Document LM Studio/GGUF fallback path.
- [x] Task: Keep exports on SSD and ignored by Git.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Ollama/LM Studio' (Protocol in workflow.md)

## Phase 3: Hermes Integration

- [x] Task: Validate Hermes against local OpenAI-compatible endpoint.
- [x] Task: Record endpoint, model, latency, and limitations.
- [x] Task: Update runtime docs and runtime-card template.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Hermes Integration' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- [x] Task: Estimate track health using hub `conductor/health-score.md`.
- [ ] Task: Close or document all gaps below health 9.5.
- [x] Task: Run hub readiness validation and attach result to the track notes.
- [ ] Task: Confirm health >= 9.5 before marking this track complete.

- Current readiness result: hub readiness validation passes in the shared repo venv; `mlx_lm` and `datasets` import successfully there.
- Current health estimate: 9.6 / 10.
- Evidence: Qwen3 4B MLX adapter loaded through `mlx_lm.server`; `/v1/models` and `/v1/chat/completions` passed through `ollama-pack/scripts/runtime_smoke.sh`; runtime card recorded at `ollama-pack/runtime-card.qwen3-4b-mlx-smoke.md`.
- Gaps: Ollama/LM Studio remain pending until a GGUF export exists; specialist runtimes remain lane-specific follow-up work.
