# Specification: Qwen3 v4 Safety/Refusal Result Ingest

## Overview

Run the pinned Qwen3 v4 safety/refusal suite locally with the MLX v4 adapter,
keep raw artifacts on the external SSD, and ingest a compact, validator-backed
result report into the repo.

## Goals

- Execute the 8-case safety/refusal suite against
  `Qwen/Qwen3-4B-MLX-4bit` plus the v4 targeted LoRA adapter.
- Store raw responses, results, and the summary under
  `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/`.
- Add a compact repo report with the strict score, diagnostic empty-think score,
  refusal failure IDs, and artifact paths.
- Update the official-candidate execution matrix so the safety/refusal slice is
  marked as scored evidence rather than pending runtime.
- Preserve the publication boundary: this internal suite is not a standardized
  safety benchmark or public safety readiness claim.

## Acceptance Criteria

- Produce `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v4-peft-safety-refusal-20260616/summary.json`.
- Add `scripts/build_safety_refusal_result_report.py`.
- Add `scripts/validate_safety_refusal_result_report.py`.
- Generate JSON and Markdown safety/refusal result reports under
  `reports/benchmark/official-candidates/`.
- Update the official-candidate matrix to report
  `safety-refusal` as `scored-artifact-present`.
- Add focused unit tests.
- Wire the validator into hub readiness.

## Out Of Scope

- Claiming a passing safety/refusal result.
- Running XSTest, SimpleSafetyTests, HarmBench, or other standardized safety
  suites.
- Modifying training data or launching a repair fine-tune.
- Moving raw benchmark artifacts into git.
