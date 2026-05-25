# Specification: Qwen3 0.6B ONNX Transformers.js Bridge Proof

## Overview

Prove, or fail closed on, a local Transformers.js bridge for
`onnx-community/Qwen3-Reranker-0.6B-ONNX` using SSD-backed caches and tooling
only. This track is about runtime evidence, not model promotion.

## Requirements

- Verify the ONNX reranker can be loaded through Transformers.js from a local,
  SSD-backed cache path or documented SSD-backed artifact root.
- Keep all transient caches, downloads, and tool state on `/Volumes/PortableSSD`.
- Do not add `node_modules` to the repository.
- Fail closed if the bridge cannot run cleanly, if the artifact is missing, or
  if the local runtime setup is not deterministic enough for a proof.
- Do not promote the ONNX model into any default lane until this bridge passes.
- Record the exact command line, artifact path, cache path, and runtime outcome
  for the proof attempt.

## Acceptance Criteria

- The track directory contains `spec.md`, `plan.md`, `index.md`, and
  `metadata.json`.
- `conductor/tracks.md` contains an unchecked registry entry pointing to this
  track.
- The runtime proof clearly states pass or fail-closed status for the ONNX /
  Transformers.js bridge.
- Default model promotion remains gated until the bridge proof succeeds.

## Non-Goals

- No default promotion of `onnx-community/Qwen3-Reranker-0.6B-ONNX`.
- No repo-local `node_modules` directory.
- No mem0 configuration changes.
- No broad runtime rewrites outside the bridge proof lane.
