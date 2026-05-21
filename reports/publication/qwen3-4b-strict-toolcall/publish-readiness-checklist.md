# Publish Readiness Checklist: Qwen3 4B Strict Tool-Call Heldout

## Identity

- Candidate: `qwen3-4b-strict-toolcall`
- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Training data: `gemma4/data/strict_tool_call`
- Required heldout suite: `benchmarks/tool_call_local/heldout_suite.json`
- Required strict heldout pass rate: `1.000`
- Current publication status: BLOCKED

## Required Evidence

- [x] Training config path recorded.
- [x] Exact training command recorded.
- [x] Adapter path recorded.
- [x] Effective trained tokens recorded.
- [x] Final validation loss recorded.
- [x] Peak memory and wall time recorded.
- [x] Heldout benchmark command recorded.
- [x] Raw heldout output path under `$HERMES_EVAL_ROOT` recorded.
- [ ] Strict heldout pass rate is `1.000`.
- [x] Diagnostic metrics, if present, are labeled informational only.
- [ ] License and redistribution review recorded.
- [ ] Model card benchmark numbers trace back to raw artifacts and command lines.

## Publication Gate

Publication remains blocked until the strict heldout benchmark command uses `benchmarks/tool_call_local/heldout_suite.json` and reports pass rate `1.000`.

The benchmark-overlapping `benchmarks/tool_call_local/suite.json` may be used for local regression checks, but it cannot satisfy this checklist. Diagnostic empty-think-stripped scoring may explain failures, but it cannot replace the strict heldout pass gate.

## Current Decision

BLOCKED. Training completed with 28,020 effective tokens, but the strict heldout pass rate was only `0.250`. Diagnostic empty-think-stripped pass rate was `0.750`, which is useful for debugging but cannot satisfy the publication gate.
