# Specification: Frontier Radar Corrections

## Overview

Correct the model radar so it distinguishes verified public model checkpoints from rumors, architecture families, and tooling.

## Requirements

- Remove Qwen3.7 as a current local or hosted-preview model lane until official public evidence exists.
- Record Qwen3.6 as the current verified Qwen frontier target.
- Add Hermes-4.3-36B as the newer public Hermes baseline/teacher candidate while keeping Hermes-4-14B as the smaller first baseline.
- Represent LFM2.5 as the verified public family variants rather than an invented 3B class.
- Represent BitNet, RWKV, Mamba, and RLM entries with exact public checkpoints or explicit architecture-family status.
- Keep Unsloth, KTransformers, and LEAP documented as tooling, not model names.

## Acceptance Criteria

- `MODEL_CANDIDATES.yaml` uses verified candidates and exact checkpoint names where available.
- `README.md`, `FUTURE_MODELS.md`, `FRAMEWORKS.md`, and `RUNTIME_TARGETS.md` reflect the corrected taxonomy.
- Unsupported Qwen3.7 references are phrased only as a guardrail, not a runnable lane.
- No model weights are downloaded.

## Out Of Scope

- Running new model downloads.
- Fine-tuning new frontier candidates.
- Publishing model artifacts.
