# Plan: Tiny Helper Role Repair

## Phase 1: Candidate Confirmation

- [ ] Task: verify the exact Hugging Face IDs and packaging lanes for the tiny
  helper candidates.
- [ ] Task: confirm the helper/extraction scope in `MODEL_CANDIDATES.yaml` and
  related radar docs.
- [ ] Task: identify the comparison baseline and the expected strict Hermes
  behavior for each candidate.

## Phase 2: Runtime Proof And Repair

- [ ] Task: run or record bounded strict-format smokes for the tiny helper
  candidates.
- [ ] Task: compare the outputs against the Hermes helper/extraction role
  criteria.
- [ ] Task: add the smallest prompt/profile or scoring wrapper change needed to
  make the best lane reproducible.

## Phase 3: Evidence And Documentation

- [ ] Task: write the benchmark report and update the handoff notes.
- [ ] Task: update the relevant model radar and roadmap references.
- [ ] Task: run validation for candidate, docs, and whitespace checks.
- [ ] Task: mark the track complete only after the evidence is documented.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.5 / 10
- Evidence: the repository already has live runtime evidence for MiniCPM5-1B,
  Qwen3.5-0.8B, Qwen3.5-2B, and EXAONE 1.2B; this track exists to convert that
  evidence into a clearly documented helper lane.
- Gaps: no strict helper winner has been codified yet, and the best prompt /
  profile repair path still needs to be finalized.
