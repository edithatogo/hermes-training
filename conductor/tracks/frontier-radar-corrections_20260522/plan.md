# Plan: Frontier Radar Corrections

## Phase 1 - Model Verification Corrections

- [x] Task: Remove Qwen3.7 as a current model lane.
- [x] Task: Add Hermes-4.3-36B as a newer public Hermes baseline candidate.
- [x] Task: Expand LFM2.5 to verified public variants.
- [x] Task: Replace generic RWKV/BitNet/RLM references with exact public checkpoint names where available.

## Phase 2 - Tooling And Architecture Taxonomy

- [x] Task: Keep Unsloth, KTransformers, and LEAP as frameworks/tooling.
- [x] Task: Treat Mamba/subquadratic as architecture-family language until exact weights/runtime are verified.
- [x] Task: Update README, future model radar, runtime targets, and framework docs.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: model radar, README, future model notes, runtime targets, and framework docs now separate verified checkpoints, architecture families, and tooling.
- Decision: implemented. No new model downloads or publication actions were taken.
