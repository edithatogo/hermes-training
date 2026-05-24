# Plan: Runtime Format Ladder

## Phase 1 - Format Ladder Contract

- [x] Task: Add a machine-readable runtime/training format ladder.
    - [x] Include MLX-native training/runtime.
    - [x] Include GGUF portability/runtime.
    - [x] Include Unsloth cloud training.
    - [x] Include KTransformers MoE runtime/training.
    - [x] Include Liquid LEAP/LFM edge runtime/training.
    - [x] Include recurrent, SSM, BitNet, and recursive research runtimes.
    - [x] Include hosted frontier API teacher/evaluator use.

## Phase 2 - Validation

- [x] Task: Add validator for required lanes, fields, environments, and proof lists.
- [x] Task: Wire the validator into hub readiness checks.
- [x] Task: Run validation.

## Phase 3 - Documentation And Conductor Sync

- [x] Task: Update requirements with the format-agnostic strategy.
- [x] Task: Update design Mermaid diagrams to show the format ladder.
- [x] Task: Update contracts with a format-lane contract.
- [x] Task: Update runtime targets and README so GGUF is described as a portability lane.
- [x] Task: Update model candidate notes where needed.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: `RUNTIME_FORMAT_LANES.yaml`, `scripts/validate_runtime_format_lanes.py`, `scripts/validate_readiness.py`, `conductor/requirements.md`, `conductor/design.md`, `conductor/contracts.md`, `conductor/tech-stack.md`, `README.md`, and `RUNTIME_TARGETS.md` now make GGUF one lane in a broader format strategy.
- Remaining gaps: Runtime proof is still required before KTransformers, LEAP, RWKV, BitNet, Mamba/SSM, recursive, or hosted frontier lanes can produce Hermes readiness claims.
