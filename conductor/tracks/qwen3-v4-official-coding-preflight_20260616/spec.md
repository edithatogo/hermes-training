# Specification: Qwen3 v4 Official Coding Preflight

## Overview

Prepare the official coding benchmark slice for the promoted Qwen3 v4 Hermes
adapter. This track validates the EvalPlus/HumanEval execution harness and the
expected generated-solutions handoff without executing benchmark tests or
claiming pass@k.

## Goals

- Correct the official-candidate coding command for the installed EvalPlus
  interface.
- Verify the SSD-backed benchmark Python and EvalPlus CLI are available.
- Verify `evalplus` and `human_eval` imports in the benchmark environment.
- Verify the generated solutions JSONL handoff path and record whether it is
  ready.
- Record a dated preflight report under the official-candidates report tree.
- Wire validation into hub readiness so command-shape drift fails closed.

## Acceptance Criteria

- Update the official-candidate queue so `official-coding` uses
  `python -m evalplus.evaluate humaneval --samples ...`.
- Add `scripts/check_official_coding_preflight.py` and a matching validator.
- Add unit tests for missing-generated-solutions and ready-to-evaluate states.
- Store compact JSON/Markdown preflight reports in Git.
- Keep `official-coding` marked missing until executed scores exist.
- Keep all future generated solutions and scores under
  `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/`.
- Run focused tests and hub readiness validation.

## Out Of Scope

- Generating model code completions.
- Running HumanEval/EvalPlus execution.
- Reporting pass@1 or pass@k.
- Starting cloud compute or creating hosted endpoints.
