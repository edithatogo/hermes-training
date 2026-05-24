# Plan: Runtime Proof Completion

## Dependency Map

- Phase 1 is the shared prerequisite for all runtime work.
- Phase 2A, Phase 2B, and Phase 2C can run in parallel after Phase 1.
- Phase 3 can run after any one upstream runtime smoke from Phase 2 succeeds.
- Phase 4 must not start until an Ollama runtime upgrade or installation change is recorded.
- Phase 5 closes the track after all unblocked runtime evidence is recorded.

## SSD Artifact Policy

- Use `/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/` for run cards, logs, summaries, and captured responses.
- Reuse existing model artifacts already on `/Volumes/PortableSSD`; do not download large models.
- Keep model weights, GGUFs, merged exports, caches, and generated evaluation outputs out of Git.
- Record missing artifacts as blockers instead of fetching them.

## Phase 1 - Scope, Inventory, And Shared Harness

- [x] Task: Confirm runtime proof inputs and SSD roots.
    - [x] Source `scripts/env.sh` before any hub-level runtime command.
    - [x] Create or reserve `/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/`.
    - [x] Reconfirm the existing Qwen3 `Q4_K_M` GGUF path from `RUNTIME_TARGETS.md`.
    - [x] Inventory local Hermes 4 14B and Qwen3.6 artifacts or active endpoints without downloading anything.
    - [x] Record the artifact inventory in the track run notes.
- [x] Task: Confirm validation commands are ready.
    - [x] Run `./.venv/bin/python scripts/openai_normalizing_proxy.py --self-test`.
    - [x] Identify the smallest reusable non-streaming OpenAI-compatible chat smoke command.
    - [x] Define the run-card fields for endpoint URL, model ID, runtime version, artifact path, prompt, response shape, and pass/fail result.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Scope, Inventory, And Shared Harness' (Protocol in workflow.md)

## Phase 2A - LM Studio Proof For Existing Qwen3 Q4_K_M GGUF

- [ ] Task: Validate the existing Qwen3 GGUF through LM Studio.
    - [ ] Start LM Studio server on `http://localhost:1234/v1` or record the active LM Studio endpoint.
    - [ ] Load `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`.
    - [ ] Run `GET /v1/models` and one non-streaming `POST /v1/chat/completions`.
    - [ ] Capture response shape, model ID, and any Qwen empty-think behavior.
    - [ ] Write the LM Studio Qwen3 run card under the SSD runtime-proof-completion root.
- [ ] Task: Conductor - Automated Review and Checkpoint 'LM Studio Proof For Existing Qwen3 Q4_K_M GGUF' (Protocol in workflow.md)

## Phase 2B - Hermes 4 14B Runtime Proof

- [ ] Task: Prove or block Hermes 4 14B runtime without large downloads.
    - [ ] Check for an existing Hermes 4 14B local artifact under SSD-backed model, GGUF, Ollama, LM Studio, or cache roots.
    - [ ] Check for an already-running OpenAI-compatible endpoint that serves a Hermes 4 14B model.
    - [ ] If a local artifact or endpoint exists, run one Hermes-style non-streaming chat smoke.
    - [ ] If no artifact or endpoint exists, record the no-download blocker with exact checked paths and endpoints.
    - [ ] Write the Hermes 4 14B run card under the SSD runtime-proof-completion root.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Hermes 4 14B Runtime Proof' (Protocol in workflow.md)

## Phase 2C - Qwen3.6 Runtime Proof

- [ ] Task: Prove or block Qwen3.6 runtime without large downloads.
    - [ ] Check for an existing Qwen3.6 local artifact under SSD-backed model, GGUF, Ollama, LM Studio, KTransformers, or cache roots.
    - [ ] Check for an already-running OpenAI-compatible endpoint that serves Qwen3.6.
    - [ ] If a local artifact or endpoint exists, run one non-streaming chat smoke with a realistic short context.
    - [ ] If no artifact or endpoint exists, record the no-download blocker with exact checked paths and endpoints.
    - [ ] Write the Qwen3.6 run card under the SSD runtime-proof-completion root.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Qwen3.6 Runtime Proof' (Protocol in workflow.md)

## Phase 3 - OpenAI Normalizing Proxy Route

- [ ] Task: Route a validated runtime through the OpenAI normalizing proxy.
    - [ ] Select the first successful upstream from Phase 2A, Phase 2B, or Phase 2C.
    - [ ] Start `scripts/openai_normalizing_proxy.py` against that upstream on a free local port.
    - [ ] Run `GET /v1/models` through the proxy.
    - [ ] Run one non-streaming `POST /v1/chat/completions` through the proxy.
    - [ ] Confirm streaming requests remain rejected unless the proxy contract changes in a separate track.
    - [ ] Record that proxy-normalized output is runtime integration evidence only.
- [ ] Task: Conductor - Automated Review and Checkpoint 'OpenAI Normalizing Proxy Route' (Protocol in workflow.md)

## Phase 4 - Deferred Ollama Retest After Runtime Upgrade

- [ ] Task: Gate the Ollama Qwen3 retest on a concrete runtime upgrade.
    - [ ] Check and record current Ollama version and installation source.
    - [ ] Proceed only if a runtime upgrade, rebuild, or installation change occurred after the earlier Qwen3 GGUF import failure.
    - [ ] If no upgrade occurred, mark the Ollama retest blocked and do not rerun the failing import.
- [ ] Task: Retest Qwen3 GGUF in Ollama only after the gate passes.
    - [ ] Reuse the existing SSD-backed Qwen3 `Q4_K_M` GGUF.
    - [ ] Run the smallest Ollama create/import command needed for the current runtime.
    - [ ] Run one OpenAI-compatible chat smoke through `http://127.0.0.1:11434/v1` if import succeeds.
    - [ ] Record daemon stability, model visibility, endpoint result, and rollback notes.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Deferred Ollama Retest After Runtime Upgrade' (Protocol in workflow.md)

## Phase 5 - Documentation, Registry, And Closeout

- [ ] Task: Update minimal runtime documentation only where needed.
    - [ ] Point `RUNTIME_TARGETS.md` or a run-card index at the new SSD-backed run cards if runtime evidence changed.
    - [ ] Preserve the no-large-download policy and the strict benchmark versus runtime integration boundary.
    - [ ] Avoid duplicating large logs in Git.
- [ ] Task: Run validation.
    - [ ] Run `./.venv/bin/python scripts/validate_readiness.py`.
    - [ ] Run any syntax checks touched by the track.
    - [ ] Update this plan with completed statuses and remaining blockers.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Documentation, Registry, And Closeout' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.1 / 10
- Evidence: `reports/runtime/runtime-inventory-20260524.md` records current endpoints, SSD GGUF artifacts, normalizing proxy self-test, and no-download frontier artifact blockers. LM Studio and MLX endpoint proof remain blocked because those servers are not listening.
