# Plan: Prompt/Profile Repair Experiments

## Phase 1 - Runner Controls

- [x] Task: Add local MLX system prompt controls.
  - [x] Add `--system-prefix` and `--system-suffix` to the local pilot runner.
  - [x] Preserve raw responses, score-only responses, and strict scoring.

## Phase 2 - Experiment Matrix

- [x] Task: Generate concrete repair experiment variants.
  - [x] Build variants from the existing prompt/profile repair queue.
  - [x] Emit no-download local and endpoint commands.
  - [x] Mark score-normalizer variants as analysis-only.

## Phase 3 - Validation And Documentation

- [x] Task: Add focused unit tests.
- [x] Task: Add deterministic report validation and readiness wiring.
- [x] Task: Generate reports and update handoff/registry.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: The experiment matrix is deterministic, strict, no-download, and
  explicit about analysis-only normalizers.
- Validation: Focused unit tests, experiment validator, Conductor consistency,
  and full readiness are required before commit.
- Gaps: No repair experiments were executed in this track.
- Decision: Complete. The next local work can run one concrete experiment at a
  time without inventing prompt/profile flags during execution.
