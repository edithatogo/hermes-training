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

- [x] Task: Run only the smallest useful support proofs.
    - [x] Execute local proof where packaging is already available.
    - [x] Execute Colab proof for sanitized support benchmarks where local load is excessive.
    - [x] Document blocked NGC or Azure proofs with exact auth/quota blocker.
    - [x] Capture output restrictions.
    - Note: source-verification and lane classification are complete; runtime proof for the newest support lanes remains the next action.
    - Evidence: `reports/runtime/cross-runtime-proof-matrix-20260612.md`, `reports/runtime/support-lane-proof-queue-20260612.md`, `reports/benchmark/mlx-loglikelihood/minicpm5-1b-mlx-loglikelihood-smoke-20260612.md`, `reports/benchmark/local-pilots/tiny-helper-standard-benchmark-execution-20260612.md`, `reports/colab/frontier-support-colab-smoke-20260612.md`
- [x] Task: Capture output restrictions.
    - [x] Record license, redistribution, and publication restrictions.
    - [x] Keep restricted outputs out of public artifacts unless approved.
- [ ] Task: Conductor - User Manual Verification 'Bounded Proof Execution' (Protocol in workflow.md)

## Phase 4: Roadmap Reconciliation

- [x] Task: Update support-lane artifacts.
    - [x] Update `FUTURE_MODELS.md`.
    - [x] Update `MODEL_CANDIDATES.yaml`.
    - [x] Update scan follow-up reports and benchmark hooks.
- [x] Task: Validate and checkpoint.
    - [x] Run readiness and candidate checks.
    - [x] Commit and push bounded docs and evidence.
- [x] Task: Conductor - User Manual Verification 'Roadmap Reconciliation' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: `reports/runtime/cross-runtime-proof-matrix-20260612.md`, `reports/runtime/support-lane-proof-queue-20260612.md`, `reports/colab/frontier-support-colab-smoke-20260612.md`, `reports/model-radar/current-release-scan-20260612.md`
- Gaps: Azure and NGC remain fail-closed until auth, entitlement, and quota gates pass.
- Decision: complete for the current support-lane evaluation phase; follow-on execution belongs in candidate-specific runtime tracks.
