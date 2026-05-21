# Plan: Qwen3.6 Runtime Proof and Qwen3.7 Hosted-Preview Watchlist

## Phase 1 - Scope and SSD Guardrails

- [ ] Task: Confirm the runtime proof will use only existing SSD-backed artifacts and documented endpoints
  - [ ] List the current Qwen3.6 and Hermes 4 runtime candidates from `RUNTIME_TARGETS.md`
  - [ ] Identify any existing local paths before touching runtime commands
  - [ ] Keep every note and artifact path under `/Volumes/PortableSSD`
- [ ] Task: Conductor - Automated Review and Checkpoint 'Scope and SSD Guardrails' (Protocol in workflow.md)

## Phase 2 - Qwen3.6 and Hermes 4 Runtime Proof

- [ ] Task: Run the Qwen3.6 runtime smoke without new downloads
  - [ ] Prefer an existing GGUF, MLX, Ollama, or documented local path already on SSD
  - [ ] Validate endpoint reachability and one parseable chat completion if the artifact is available
  - [ ] Record any runtime gap instead of downloading a new model
- [ ] Task: Run the Hermes 4 runtime smoke without new downloads
  - [ ] Prefer an existing GGUF or documented local path already on SSD
  - [ ] Validate endpoint reachability and one Hermes-style prompt smoke if the artifact is available
  - [ ] Record any runtime gap instead of downloading a new model
- [ ] Task: Conductor - Automated Review and Checkpoint 'Qwen3.6 and Hermes 4 Runtime Proof' (Protocol in workflow.md)

## Phase 3 - Qwen3.7 Hosted-Preview Watchlist

- [ ] Task: Lock Qwen3.7 into hosted-preview watchlist status
  - [ ] Track `Qwen/Qwen3.7-Max`
  - [ ] Track `Qwen/Qwen3.7-Plus-Preview`
  - [ ] Keep the policy explicitly hosted-api-only with no local download plan
- [ ] Task: Update radar and runtime docs with the next-track summary and SSD-first guardrails
  - [ ] Sync `MODEL_CANDIDATES.yaml`
  - [ ] Sync `FUTURE_MODELS.md`
  - [ ] Sync `RUNTIME_TARGETS.md`
  - [ ] Sync `conductor/tracks.md`
- [ ] Task: Conductor - Automated Review and Checkpoint 'Qwen3.7 Hosted-Preview Watchlist' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.5 / 10
- Evidence: track scope is concrete, downloads are blocked by design, and the watchlist/runtime split is explicit.
- Decision: ready to start once existing SSD-backed artifacts and endpoint commands are confirmed.
