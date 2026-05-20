# Specification: Runtime Packaging and Hermes Validation

## Overview

Ensure promoted adapters can be used through practical local runtimes: MLX server first, then Ollama and LM Studio/GGUF where supported. Document the exact runtime card template, endpoint smoke matrix, and SSD artifact policy so the run notes are reproducible.

## Requirements

- Validate runtime path after benchmark promotion.
- Keep merged models, GGUFs, and runtime exports on SSD-backed paths.
- Provide Hermes-compatible endpoint instructions.
- Provide a runtime card template that records command, endpoint, smoke prompt, result, and limitations.
- Provide an endpoint smoke matrix for MLX, Ollama, and LM Studio.
- Keep merged models, GGUFs, and runtime exports on SSD-backed paths.
- Record runtime smoke results in run/model cards.

## Acceptance Criteria

- Runtime smoke script runs for available packaged models.
- Documentation states exact command, endpoint, model name, and limitations.
- Artifacts remain ignored unless intentionally published.

## Out of Scope

- Packaging unbenchmarked adapters as release artifacts.
- Full runtime performance bakeoff across every candidate model.
