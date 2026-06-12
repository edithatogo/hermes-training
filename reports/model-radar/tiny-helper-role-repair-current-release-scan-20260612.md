# Tiny Helper Role Repair - 2026-06-12

## Summary

This track converted the existing tiny-model runtime evidence into a reproducible
helper/extraction lane for Hermes work on the MacBook Pro M1 Max / 32 GB
environment.

The result is not a strict Hermes publication lane. It is a documented
comparison lane for the smallest local candidates that have already been
runtime-proven.

## Decision

Use `tiny-helper-no-prefill` from `RUNTIME_PROMPT_PROFILES.yaml` as the
documented helper/extraction lane for:

- `Qwen/Qwen3.5-0.8B`
- `Qwen/Qwen3.5-2B`
- `openbmb/MiniCPM5-1B-MLX`

Keep `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF` as a comparison lane only.

## Evidence

| Candidate | Evidence | Outcome |
|---|---|---|
| `Qwen/Qwen3.5-0.8B` | `reports/benchmark/mlx-loglikelihood/qwen35-08b-mlx-loglikelihood-smoke-20260612.md` | Runtime/load proven; raw tiny BFCL-style helper gate failed strict tool-call formatting. |
| `Qwen/Qwen3.5-2B` | `reports/benchmark/mlx-loglikelihood/qwen35-2b-mlx-loglikelihood-smoke-20260612.md` | Runtime/load proven; raw tiny BFCL-style helper gate failed strict tool-call formatting. |
| `openbmb/MiniCPM5-1B-MLX` | `reports/benchmark/mlx-loglikelihood/minicpm5-1b-mlx-loglikelihood-smoke-20260612.md` | Runtime/load proven; raw tiny BFCL-style helper gate failed strict tool-call formatting. |
| `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF` | `HANDOFF.md` runtime evidence summary | Runtime evidence only; repeated-brace output is not a strict Hermes candidate. |

## Implementation Notes

- The runtime prompt profile keeps the tiny lane raw and explicit.
- No assistant prefill or empty-think normalization is applied to this lane.
- The lane is for helper/extraction comparison and regression notes, not for
  strict Hermes publication claims.

## Validation

- `scripts/validate_runtime_prompt_profiles.py`
- `scripts/check_model_candidates.py`
- `git diff --check`

## Status

Complete as a documentation and contract repair track.
