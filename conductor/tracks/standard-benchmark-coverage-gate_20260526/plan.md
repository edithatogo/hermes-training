# Plan: Standard Benchmark Coverage Gate

## Phase 1: Conductor Boundary

- [x] Task: populate the existing `standard-benchmark-coverage-gate_20260526`
  track directory with spec, plan, index, and metadata.
- [x] Task: register the track in `conductor/tracks.md`.

## Phase 2: Harness Interface Alignment

- [x] Task: update the BFCL pilot manifest to use the installed
  `/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl generate`
  and `bfcl evaluate` commands.
- [x] Task: add a static manifest validator for BFCL and lm-eval command
  surfaces.
- [x] Task: wire the validator into readiness checks.

## Phase 3: lm-eval Bridge Preparation

- [x] Task: extend the OpenAI normalizing proxy to pass through
  `/v1/completions`.
- [x] Task: coerce integer OpenAI `logprobs` requests to boolean for
  `mlx_lm.server` compatibility.
- [x] Task: keep chat-completion normalization behavior unchanged.

## Phase 4: Radar Consistency

- [x] Task: update LFM2-24B and LFM2.5 runtime-proof wording.
- [x] Task: clarify mem0 Qwen reranker source-model evidence versus ONNX
  packaging blocker.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: stale BFCL command forms are guarded, the logprobs bridge has a
  self-test path, model-radar wording matches current runtime proof cards, and
  validation passes without writing large artifacts.
- Remaining gap: this is bridge/readiness work. The official benchmark scores
  still require live endpoint runs and separate run cards under the SSD eval
  root.
