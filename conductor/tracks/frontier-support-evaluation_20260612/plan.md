# Frontier Teacher and Support Lane Evaluation Plan

## Phase 1: Support-Lane Source Audit

- [ ] Task: Read the completed scan report and roadmap entries.
    - [ ] Extract teacher/reference models.
    - [ ] Extract NVIDIA/NGC opportunities.
    - [ ] Extract multimodal, audio, ASR, TTS, omni, and packaging candidates.
- [ ] Task: Assign explicit roles.
    - [ ] Mark candidates as teacher, evaluator, retriever, multimodal extractor, audio support, packaging proof, or watchlist.
    - [ ] Flag candidates that are not local fine-tune targets.
- [ ] Task: Conductor - User Manual Verification 'Support-Lane Source Audit' (Protocol in workflow.md)

## Phase 2: Evaluation Design

- [ ] Task: Define support-lane benchmark hooks.
    - [ ] Map teacher models to data-generation or comparison tasks.
    - [ ] Map multimodal models to retrieval or evidence extraction tests.
    - [ ] Map audio/ASR/TTS models to future support harnesses.
- [ ] Task: Define backend policies.
    - [ ] Prefer Colab for bounded, sanitized experiments.
    - [ ] Use NGC only after API-key and entitlement checks.
    - [ ] Use Azure only after subscription and quota checks.
- [ ] Task: Conductor - User Manual Verification 'Evaluation Design' (Protocol in workflow.md)

## Phase 3: Bounded Proof Execution

- [ ] Task: Run only the smallest useful support proofs.
    - [ ] Execute local proof where packaging is already available.
    - [ ] Execute Colab proof for sanitized support benchmarks where local load is excessive.
    - [ ] Document blocked NGC or Azure proofs with exact auth/quota blocker.
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
