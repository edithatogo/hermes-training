# Frontier Teacher and Support Lane Evaluation Plan

## Phase 1: Support-Lane Source Audit

- [x] Task: Read the completed scan report and roadmap entries.
    - [x] Extract teacher/reference models.
    - [x] Extract NVIDIA/NGC opportunities.
    - [x] Extract multimodal, audio, ASR, TTS, omni, and packaging candidates.
    - Evidence: `reports/model-radar/current-release-scan-20260612.md`, `reports/model-radar/support-lane-surface-refresh-current-release-scan-20260612.md`, `reports/model-radar/asr-support-follow-up-current-release-scan-20260612.md`, `reports/model-radar/tts-support-follow-up-current-release-scan-20260612.md`, `reports/model-radar/multimodal-support-follow-up-current-release-scan-20260612.md`, `reports/model-radar/nvidia-physical-ai-follow-up-current-release-scan-20260612.md`
- [x] Task: Assign explicit roles.
    - [x] Mark candidates as teacher, evaluator, retriever, multimodal extractor, audio support, packaging proof, or watchlist.
    - [x] Flag candidates that are not local fine-tune targets.
    - Evidence: `MODEL_CANDIDATES.yaml`, `FUTURE_MODELS.md`, `reports/model-radar/current-release-scan-20260612.md`
- [x] Task: Conductor - User Manual Verification 'Support-Lane Source Audit' (Protocol in workflow.md)

## Phase 2: Evaluation Design

- [x] Task: Define support-lane benchmark hooks.
    - [x] Map teacher models to data-generation or comparison tasks.
    - [x] Map multimodal models to retrieval or evidence extraction tests.
    - [x] Map audio/ASR/TTS models to future support harnesses.
    - Evidence: `reports/model-radar/current-release-scan-20260612.md`, `reports/model-radar/nvidia-physical-ai-follow-up-current-release-scan-20260612.md`, `reports/model-radar/asr-support-follow-up-current-release-scan-20260612.md`, `reports/model-radar/tts-support-follow-up-current-release-scan-20260612.md`, `reports/model-radar/multimodal-support-follow-up-current-release-scan-20260612.md`
- [x] Task: Define backend policies.
    - [x] Prefer Colab for bounded, sanitized experiments.
    - [x] Use NGC only after API-key and entitlement checks.
    - [x] Use Azure only after subscription and quota checks.
    - Evidence: `COLAB_SCALEOUT.md`, `AZURE_SCALEOUT.md`, `scripts/colab_preflight.py`, `scripts/colab_dispatch.py`
- [x] Task: Conductor - User Manual Verification 'Evaluation Design' (Protocol in workflow.md)

## Phase 3: Bounded Proof Execution

- [~] Task: Run only the smallest useful support proofs.
    - [ ] Execute local proof where packaging is already available.
    - [ ] Execute Colab proof for sanitized support benchmarks where local load is excessive.
    - [ ] Document blocked NGC or Azure proofs with exact auth/quota blocker.
    - Note: source-verification and lane classification are complete; runtime proof for the newest support lanes remains the next action.
    - Evidence: `reports/runtime/cross-runtime-proof-matrix-20260612.md`
- [ ] Task: Capture output restrictions.
    - [ ] Record license, redistribution, and publication restrictions.
    - [ ] Keep restricted outputs out of public artifacts unless approved.
- [ ] Task: Conductor - User Manual Verification 'Bounded Proof Execution' (Protocol in workflow.md)

## Phase 4: Roadmap Reconciliation

- [ ] Task: Update support-lane artifacts.
    - [ ] Update `FUTURE_MODELS.md`.
    - [ ] Update `MODEL_CANDIDATES.yaml`.
    - [ ] Update scan follow-up reports and benchmark hooks.
- [ ] Task: Validate and checkpoint.
    - [ ] Run readiness and candidate checks.
    - [ ] Commit and push bounded docs and evidence.
- [ ] Task: Conductor - User Manual Verification 'Roadmap Reconciliation' (Protocol in workflow.md)
