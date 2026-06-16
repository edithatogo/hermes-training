# Specification: Qwen3 v4 Safety/Refusal Suite

## Overview

Materialize a pinned safety/refusal benchmark manifest for the promoted Qwen3 v4
Hermes adapter. The suite focuses on unavailable and disallowed tool requests
while retaining valid tool-call controls required by the existing local scorer.

## Goals

- Correct the official-candidate queue command to use
  `run_tool_call_benchmark.py --suite`.
- Build a versioned safety/refusal suite under `reports/benchmark/manifests/`.
- Include invalid/disallowed-tool refusal cases with explicit forbidden-marker
  checks.
- Include control cases for JSON validity, argument correctness, and multi-turn
  repair so the existing scorer contract remains valid.
- Add validation and focused unit tests.
- Keep the official-candidate coverage status missing until scored artifacts
  exist.

## Acceptance Criteria

- Add `scripts/materialize_safety_refusal_suite.py`.
- Add `scripts/validate_safety_refusal_suite.py`.
- Generate `reports/benchmark/manifests/safety-refusal-suite-20260616.json`.
- Generate `reports/benchmark/manifests/safety-refusal-suite-20260616.md`.
- Run `scripts/run_tool_call_benchmark.py --suite ... --dry-run`.
- Wire validation into hub readiness.
- Run focused tests and hub readiness validation.

## Out Of Scope

- Running the suite against a model.
- Claiming safety/refusal benchmark performance.
- Publishing new model or dataset artifacts.
- Changing the promoted Hermes model decision.
