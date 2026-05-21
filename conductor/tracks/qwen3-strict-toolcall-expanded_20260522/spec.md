# Specification: Qwen3 Strict Tool-Call Expanded Data Retrain

## Overview

Create the next Qwen3 4B strict tool-call promotion attempt after the failed held-out run. This track expands strict tool-call training data, audits it for held-out contamination and coverage, attempts a retrain, evaluates against the held-out gate, and records a publication decision.

This track began as scaffolding and then executed the authorized local implementation. It does not authorize Hugging Face publication because the held-out strict gate remains failed.

## Requirements

- Expand `gemma4/data/strict_tool_call` with materially broader strict tool-call examples before retraining.
- Keep `benchmarks/tool_call_local/heldout_suite.json` completely held out; do not copy held-out prompts, expected arguments, or answer strings into training data.
- Audit the expanded data for split counts, tool coverage, invalid-tool handling, multi-call coverage, repair cases, argument exactness, and likely overlap with held-out cases.
- Retrain from `Qwen/Qwen3-4B-MLX-4bit` only after the expanded data audit is recorded.
- Keep generated adapters, caches, and benchmark outputs on `/Volumes/PortableSSD`.
- Evaluate the retrained adapter with `benchmarks/tool_call_local/heldout_suite.json` and `/no_think`.
- Preserve strict scoring as the publication gate; diagnostic empty-think-stripped metrics may be recorded as informational only.
- Block publication unless the strict held-out pass rate is exactly `1.000`.
- Document the exact data revision, audit summary, training config, training command, adapter path, benchmark command, harness revision, raw output path, and publication decision.

## Acceptance Criteria

- A Conductor track exists for expanded strict data, audit, retrain, held-out gate, and publication decision phases.
- Expanded strict tool-call seed data and deterministic materialized splits exist under `gemma4/data/strict_tool_call/`.
- A publication scaffold exists under `reports/publication/qwen3-4b-strict-toolcall-expanded/`.
- The publication checklist stays BLOCKED unless strict held-out pass rate is `1.000`.
- The run card records expanded-data audit, retrain evidence, held-out results, and final decision.
- Repo-level benchmarking and documentation plans name the expanded strict-data attempt and preserve the held-out-only publication rule.
- GitHub reproducibility assets may be committed and pushed. Hugging Face adapter, dataset, merged-weight, and GGUF publication remains out of scope until the gate passes.

## Out of Scope

- Publishing adapters, merged weights, GGUF files, datasets, or model cards.
- Weakening the strict held-out gate with diagnostic normalization scores.
- Treating mirrored-suite or training-overlapping results as publication evidence.
