# Plan: Qwen3 V4 MLX To PEFT Conversion

## Phase 1 - Converter

- [x] Task: Add a converter from MLX LoRA safetensors to PEFT-shaped safetensors.
- [x] Task: Add unit tests for key mapping, config generation, and tensor transposition.

## Phase 2 - Artifact And Report

- [x] Task: Generate the experimental PEFT-shaped adapter package on the SSD.
- [x] Task: Record the conversion report and claim boundary.
- [x] Task: Run focused tests and hub readiness validation.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: converter unit tests pass; the conversion report records 112 input keys mapped to 112 PEFT-shaped output keys across layers 28-35.
- Gaps: PEFT load/equivalence is not proven yet, so this artifact is not benchmark-ready.
- Decision: Complete as an experimental conversion step. The next track must test load/behavior before cloud scorecard use.
