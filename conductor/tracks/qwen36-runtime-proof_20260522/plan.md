# Plan: Qwen3.6 Runtime Proof and Unsupported Qwen3.7 Guardrail

## Phase 1 - Scope and SSD Guardrails

- [x] Task: Confirm the runtime proof will use only existing SSD-backed artifacts and documented endpoints
  - [x] List the current Qwen3.6 and Hermes 4 runtime candidates from `RUNTIME_TARGETS.md`
  - [x] Identify any existing local paths before touching runtime commands
  - [x] Keep every note and artifact path under `/Volumes/PortableSSD`
- [x] Task: Conductor - Automated Review and Checkpoint 'Scope and SSD Guardrails' (Protocol in workflow.md)

## Phase 2 - Qwen3.6 and Hermes 4 Runtime Proof

- [x] Task: Run the Qwen3.6 runtime smoke without new downloads
  - [x] Prefer an existing GGUF, MLX, Ollama, or documented local path already on SSD
  - [x] Validate endpoint reachability and one parseable chat completion if the artifact is available
  - [x] Record any runtime gap instead of downloading a new model
- [x] Task: Run the Hermes 4 runtime smoke without new downloads
  - [x] Prefer an existing GGUF or documented local path already on SSD
  - [x] Validate endpoint reachability and one Hermes-style prompt smoke if the artifact is available
  - [x] Record any runtime gap instead of downloading a new model
- [x] Task: Conductor - Automated Review and Checkpoint 'Qwen3.6 and Hermes 4 Runtime Proof' (Protocol in workflow.md)

## Phase 3 - Unsupported Qwen3.7 Guardrail

- [x] Task: Keep Qwen3.7 out of local lanes until official public evidence exists
  - [x] Record that no official public open-weight repo was verified
  - [x] Keep the policy explicitly no local download and no local fine-tune
- [x] Task: Update radar and runtime docs with the next-track summary and SSD-first guardrails
  - [x] Sync `MODEL_CANDIDATES.yaml`
  - [x] Sync `FUTURE_MODELS.md`
  - [x] Sync `RUNTIME_TARGETS.md`
  - [x] Sync `conductor/tracks.md`
- [x] Task: Conductor - Automated Review and Checkpoint 'Unsupported Qwen3.7 Guardrail' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: no-download artifact scan completed; no Qwen3.6 or Hermes local artifact was found; Qwen3.7 is not treated as a verified public local lane; runtime gap is documented in `reports/runtime/qwen36-hermes4-runtime-proof/run-card.md`.
- Decision: complete as a no-download runtime proof. Next pass requires an explicit artifact selection or endpoint before smoke execution.
