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
    - [x] Record whether LM Studio server is active on `http://localhost:1234/v1`.
    - [x] Load `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`.
    - [x] Run `GET /v1/models` and one non-streaming `POST /v1/chat/completions`.
    - [x] Capture response shape, model ID, and Qwen empty-think behavior.
    - [x] Write the LM Studio Qwen3 run card under the SSD runtime-proof-completion root.
    - [x] Blocker cleared: LM Studio `0.4.14+4` installed, `lms` linked on `PATH`, server passed on `127.0.0.1:1234`, and the model is loaded via SSD symbolic link.
    - [x] Benchmark recorded in `reports/benchmark/endpoint-tool-call/qwen3-q4km-lmstudio-heldout-20260524.md`.
- [ ] Task: Conductor - Automated Review and Checkpoint 'LM Studio Proof For Existing Qwen3 Q4_K_M GGUF' (Protocol in workflow.md)

## Phase 2A.1 - llama.cpp Proof For Existing Qwen3 Q4_K_M GGUF

- [x] Task: Validate the existing Qwen3 GGUF through llama.cpp.
    - [x] Build `/Volumes/PortableSSD/GitHub/llama.cpp/build/bin/llama-server`.
    - [x] Record the external llama.cpp local include patch required for the build.
    - [x] Serve `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf` on `http://127.0.0.1:8091/v1`.
    - [x] Run `GET /v1/models` and one non-streaming `POST /v1/chat/completions`.
    - [x] Capture runtime evidence in `reports/runtime/llamacpp-qwen3-q4km-server-smoke-20260524.md`.
    - [x] Run the held-out endpoint benchmark and record `reports/benchmark/endpoint-tool-call/qwen3-q4km-llamacpp-heldout-20260524.md`.

## Phase 2B - Hermes 4 14B Runtime Proof

- [x] Task: Prove or block Hermes 4 14B runtime without large downloads.
    - [x] Check for an existing Hermes 4 14B local artifact under SSD-backed model, GGUF, Ollama, LM Studio, or cache roots.
    - [x] Check for an already-running OpenAI-compatible endpoint that serves a Hermes 4 14B model.
    - [x] If a local artifact or endpoint exists, run one Hermes-style non-streaming chat smoke.
    - [x] If no artifact or endpoint exists, record the no-download blocker with exact checked paths and endpoints.
    - [x] Write the Hermes 4 14B run card under the SSD runtime-proof-completion root.
    - [x] Follow-up acquisition completed under `/Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4`.
    - [x] Runtime proof recorded in `reports/runtime/hermes4-14b-q4-llamacpp-smoke-20260524.md`.
    - [x] Held-out benchmark recorded in `reports/benchmark/endpoint-tool-call/hermes4-14b-q4-llamacpp-heldout-20260524.md`.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Hermes 4 14B Runtime Proof' (Protocol in workflow.md)

## Phase 2C - Qwen3.6 Runtime Proof

- [x] Task: Prove or block Qwen3.6 runtime without large downloads.
    - [x] Check for an existing Qwen3.6 local artifact under SSD-backed model, GGUF, Ollama, LM Studio, KTransformers, or cache roots.
    - [x] Check for an already-running OpenAI-compatible endpoint that serves Qwen3.6.
    - [x] If a local artifact or endpoint exists, run one non-streaming chat smoke with a realistic short context.
    - [x] If no artifact or endpoint exists, record the no-download blocker with exact checked paths and endpoints.
    - [x] Write the Qwen3.6 run card under the SSD runtime-proof-completion root.
    - [x] Follow-up acquisition started in `tmux` session `qwen36_download`; status recorded in `reports/runtime/qwen36-q4km-acquisition-20260524.md`.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Qwen3.6 Runtime Proof' (Protocol in workflow.md)

## Phase 3 - OpenAI Normalizing Proxy Route

- [x] Task: Route a validated runtime through the OpenAI normalizing proxy.
    - [x] Select the first successful upstream from Phase 2A, Phase 2B, or Phase 2C.
    - [x] Start `scripts/openai_normalizing_proxy.py` against that upstream on a free local port.
    - [x] Run `GET /v1/models` through the proxy.
    - [x] Run one non-streaming `POST /v1/chat/completions` through the proxy.
    - [x] Confirm streaming requests remain rejected unless the proxy contract changes in a separate track.
    - [x] Record that proxy-normalized output is runtime integration evidence only.
    - [x] Evidence exists in `reports/runtime/openai-normalizing-proxy-ollama-smoke/run-card.md`; llama.cpp direct OpenAI compatibility now also passes without the proxy.
- [ ] Task: Conductor - Automated Review and Checkpoint 'OpenAI Normalizing Proxy Route' (Protocol in workflow.md)

## Phase 4 - Deferred Ollama Retest After Runtime Upgrade

- [x] Task: Gate the Ollama Qwen3 retest on a concrete runtime upgrade.
    - [x] Check and record current Ollama version and installation source.
    - [x] Proceed only if a runtime upgrade, rebuild, or installation change occurred after the earlier Qwen3 GGUF import failure.
    - [x] If no upgrade occurred, mark the Ollama retest blocked and do not rerun the failing import.
    - [x] Current check: `/opt/homebrew/bin/ollama`, version `0.24.0`; no post-failure upgrade evidence was recorded.
- [x] Task: Retest Qwen3 GGUF in Ollama only after the gate passes.
    - [x] Reconfirm the existing SSD-backed Qwen3 `Q4_K_M` GGUF path.
    - [x] Skip the create/import command because the gate did not pass.
    - [x] Skip OpenAI-compatible chat smoke because no new Ollama import was attempted.
    - [x] Record daemon stability, model visibility, endpoint result, and rollback notes for the unchanged runtime state.
    - [x] Retest deliberately blocked because Ollama is still `0.24.0`; gate recorded in `reports/runtime/ollama-qwen3-retest-gate-20260524.md`.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Deferred Ollama Retest After Runtime Upgrade' (Protocol in workflow.md)

## Phase 5 - Documentation, Registry, And Closeout

- [x] Task: Update minimal runtime documentation only where needed.
    - [x] Point `RUNTIME_TARGETS.md` or a run-card index at the new SSD-backed run cards if runtime evidence changed.
    - [x] Preserve the no-large-download policy and the strict benchmark versus runtime integration boundary.
    - [x] Avoid duplicating large logs in Git.
- [ ] Task: Run validation.
    - [x] Run `./.venv/bin/python scripts/validate_readiness.py`.
    - [x] Run any syntax checks touched by the track.
    - [x] Update this plan with completed statuses and remaining blockers.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Documentation, Registry, And Closeout' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: `reports/runtime/runtime-inventory-20260524.md` records current endpoints, SSD GGUF artifacts, normalizing proxy self-test, and no-download frontier artifact blockers. `reports/runtime/llamacpp-qwen3-q4km-server-smoke-20260524.md` records a successful SSD-backed OpenAI-compatible llama.cpp proof for the Qwen3 Q4_K_M GGUF. `reports/runtime/hermes4-14b-q4-llamacpp-smoke-20260524.md` records successful local Hermes 4 14B Q4 runtime proof.
- Blocker: Qwen3.6 Q4_K_M acquisition is active but not complete; Gemma 4 remains paused/resumable until Qwen3.6 is proven or explicitly skipped. Hermes 4 14B Q4 is complete and runtime-proven. Ollama Qwen3 retest is intentionally blocked until a runtime upgrade or relevant local fix exists.
