# Specification: Runtime Format Ladder

## Overview

GGUF remains useful for local serving, but it must not become the implicit training or frontier-runtime strategy. This track formalizes a format/runtime ladder for Hermes-agent work so models can be evaluated in their strongest native format before optional GGUF export.

## Requirements

- Define GGUF as a portability and runtime-proof lane, not the canonical training artifact.
- Define MLX-native as the primary Mac-local training and adapter lane.
- Define Unsloth/TRL/PEFT as the cloud/CUDA training lane, gated by Azure preflight.
- Define KTransformers as a specialist large-MoE runtime and LoRA lane, gated by model-family support and reproducible launch proof.
- Define Liquid LEAP/LFM as a model-family-specific edge lane across LEAP, MLX, ONNX, and GGUF where appropriate.
- Define RWKV, BitNet, Mamba/SSM, and recursive/RLM candidates as research-runtime lanes that require native runtime proof before Hermes claims.
- Define hosted frontier APIs, including Qwen3.7-Max while no open weights are verified, as teacher/evaluator lanes only.
- Keep all large artifacts, outputs, and caches on `/Volumes/PortableSSD`.
- Add validation so the format ladder cannot silently disappear from readiness checks.

## Acceptance Criteria

- `RUNTIME_FORMAT_LANES.yaml` records the active runtime/training ladder.
- `scripts/validate_runtime_format_lanes.py` validates required lanes and fields.
- Hub readiness validation invokes the format-lane validator.
- Hub requirements, design, contracts, tech stack, runtime targets, and README describe the non-GGUF approach.
- A Conductor track records the implementation and health gate.

## Out Of Scope

- Downloading or running new models.
- Replacing the active Qwen3.6 GGUF acquisition.
- Publishing adapters or model cards.
- Claiming KTransformers, LEAP, RWKV, BitNet, Mamba, or recursive models are Hermes-ready before runtime proof.
