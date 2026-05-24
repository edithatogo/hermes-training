# Specification: Runtime Format Proof Harness

## Overview

The runtime format ladder needs a repeatable evidence workflow. This track adds a proof-card template, a generator, tests, and a manifest so GGUF, MLX, Unsloth, KTransformers, LEAP/LFM, native research runtimes, and hosted APIs can be evaluated one by one without mixing evidence types.

## Requirements

- Generate proof cards from `RUNTIME_FORMAT_LANES.yaml`.
- Default generated evidence to `/Volumes/PortableSSD/hermes-evals/runtime-format-lanes/`.
- Support preview mode without writing files.
- Preserve the boundary between runtime proof, training evidence, teacher evidence, and publication evidence.
- Validate the generator through unit tests and readiness checks.

## Acceptance Criteria

- `templates/runtime/format-lane-proof-card.md` exists.
- `scripts/create_runtime_format_lane_card.py` can render cards for all configured lanes.
- Unit tests cover validator success and card rendering.
- Runtime manifest records first proof queue and promotion rules.
- Hub readiness validation passes.

## Out Of Scope

- Running the proof cards.
- Downloading additional models.
- Publishing any model, adapter, or benchmark result.
