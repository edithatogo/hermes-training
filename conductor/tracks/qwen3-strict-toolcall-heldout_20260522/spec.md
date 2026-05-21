# Specification: Qwen3 Strict Tool-Call Heldout Promotion

## Overview

Create the promotion track for retraining Qwen3 4B on the strict tool-call dataset and evaluating the result on the non-overlapping heldout tool-call suite before any publication claim.

This track is documentation and Conductor scaffolding only. It records the required training and evaluation path; it does not authorize or run training by itself.

## Requirements

- Retrain from `Qwen/Qwen3-4B-MLX-4bit` using `gemma4/data/strict_tool_call`.
- Keep generated adapters, caches, and benchmark outputs on `/Volumes/PortableSSD`.
- Evaluate the trained adapter with `benchmarks/tool_call_local/heldout_suite.json`.
- Run the heldout benchmark with `/no_think` so the result matches the Hermes tool-call lane.
- Preserve strict scoring as the only publication gate; diagnostic empty-think-stripped metrics may be recorded but cannot promote a run.
- Block publication unless the strict heldout pass rate is exactly `1.000`.
- Document the exact training command, config path, adapter path, benchmark command, harness revision, raw output path, and promotion decision before any model-card or adapter publication.

## Acceptance Criteria

- A Conductor track exists for the strict heldout promotion pass.
- The track plan records training, evaluation, documentation, and publication decision phases without marking them complete.
- Repo-level benchmarking and documentation plans name `gemma4/data/strict_tool_call`, `benchmarks/tool_call_local/heldout_suite.json`, and the `1.000` strict heldout requirement.
- A publication checklist exists under `reports/publication/qwen3-4b-strict-toolcall/` and defaults to blocked until strict heldout pass is `1.000`.
- No training is run as part of this scaffolding task.

## Out of Scope

- Running MLX training.
- Running heldout evaluation.
- Publishing to Hugging Face.
- Weakening the strict heldout gate with diagnostic normalization scores.
- Treating benchmark-overlapping `benchmarks/tool_call_local/suite.json` results as heldout evidence.
