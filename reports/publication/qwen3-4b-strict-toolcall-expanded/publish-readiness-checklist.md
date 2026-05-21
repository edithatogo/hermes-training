# Publish Readiness Checklist: Qwen3 4B Strict Tool-Call Expanded Retrain

## Identity

- Candidate: `qwen3-4b-strict-toolcall-expanded`
- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Training data: expanded `gemma4/data/strict_tool_call`
- Required heldout suite: `benchmarks/tool_call_local/heldout_suite.json`
- Required strict heldout pass rate: `1.000`
- Current publication status: BLOCKED

## Required Evidence

- [x] Expanded strict data source policy recorded.
- [x] Expanded split generation command and seed recorded.
- [x] Dataset row counts recorded.
- [x] Dataset token audit recorded.
- [x] Tool and behavior-bucket coverage audit recorded.
- [x] Held-out contamination check recorded.
- [x] License and redistribution review recorded.
- [x] Training config path recorded.
- [x] Exact training command recorded.
- [x] Adapter path recorded.
- [x] Effective trained tokens recorded.
- [x] Final and best validation loss recorded.
- [x] Peak memory and wall time recorded.
- [x] Heldout benchmark command recorded.
- [x] Raw heldout output path under `$HERMES_EVAL_ROOT` recorded.
- [ ] Strict heldout pass rate is `1.000`.
- [x] Diagnostic metrics, if present, are labeled informational only.
- [x] Model card benchmark numbers trace back to raw artifacts and command lines.

## Publication Gate

Publication remains blocked until expanded strict data is audited, retraining is complete, and the strict heldout benchmark command uses `benchmarks/tool_call_local/heldout_suite.json` with `/no_think` and reports pass rate `1.000`.

The benchmark-overlapping `benchmarks/tool_call_local/suite.json` may be used for local regression checks, but it cannot satisfy this checklist. Diagnostic empty-think-stripped scoring may explain failures, but it cannot replace the strict heldout pass gate.

## Current Decision

BLOCKED. Expanded training completed, but held-out strict pass rate was `0.250`, below the required `1.000`. The dataset token audit and license review are now recorded, but the license review keeps Hugging Face publication blocked until upstream and mirrored-seed redistribution scope is explicitly approved.
