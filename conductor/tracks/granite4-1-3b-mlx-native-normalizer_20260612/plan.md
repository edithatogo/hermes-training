# Plan: Granite 4.1 3B Native-Normalized Local Pilot

## Phase 1: Runtime Evidence

- [x] Task: run the direct MLX load and strict BFCL-style local pilot for
  Granite 4.1 3B.
- [x] Task: run the strict pilot again with the score-only Granite native tool
  normalizer.
- [x] Task: record the raw and normalized pass rates, including the remaining
  failing case.

## Phase 2: Repository Sync

- [x] Task: add the Granite result report under `reports/benchmark/local-pilots`.
- [x] Task: update `MODEL_CANDIDATES.yaml` with the Granite runtime evidence.
- [x] Task: update `RUNTIME_FORMAT_PROOF_QUEUE.yaml` with the completed proof
  state.
- [x] Task: update `FUTURE_MODELS.md` and `HANDOFF.md` with the new status.

## Phase 3: Validation

- [x] Task: run the candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the track is complete, the raw output is preserved, and the
  normalizer is opt-in only.
- Gaps: Granite still is not a strict Hermes tool-call default.
