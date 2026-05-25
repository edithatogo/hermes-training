# Plan: Qwen3 0.6B ONNX Transformers.js Bridge Proof

## Phase 1 - Scope and Runtime Guardrails

- [ ] Task: confirm the local ONNX artifact, SSD-backed cache root, and
- [x] Task: confirm the local ONNX artifact, SSD-backed cache root, and
  Transformers.js entrypoint to use for the proof.
- [x] Task: verify the repo does not gain a `node_modules` directory and that
  any tooling install path stays outside the repository on SSD.
- [x] Task: document the fail-closed decision rule for missing artifact,
  runtime mismatch, or non-deterministic setup.

## Phase 2 - Bridge Proof

- [x] Task: run a minimal Transformers.js load or inference smoke against
  `onnx-community/Qwen3-Reranker-0.6B-ONNX`.
- [x] Task: capture exact command lines, cache paths, and the observed runtime
  behavior.
- [x] Task: record whether the bridge is pass, fail-closed, or blocked by
  missing local support.

## Phase 3 - Promotion Gate

- [x] Task: keep default model promotion disabled unless the bridge proof
  passes.
- [x] Task: update the next-step note in the track artifacts with the proof
  outcome and any follow-up requirement.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.5 / 10
- Evidence: proof runner wrote a fail-closed blocked result without creating
  repo-local `node_modules`; the CPU bridge retry with `max_length=512` timed
  out after `180.0s` before scoring one fixed-suite case.
- Gaps: future ONNX bridge retry needs a bounded CPU/CoreML proof that completes
  within the local latency budget.
