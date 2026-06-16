# Plan: Qwen3 v4 Official Coding Preflight

## Phase 1 - Command Alignment

- [x] Task: correct the official-candidate coding command to the installed
  EvalPlus positional dataset interface.
- [x] Task: strengthen queue validation so stale `--model` / `--dataset`
  command shapes fail.

## Phase 2 - Preflight Harness

- [x] Task: add `scripts/check_official_coding_preflight.py`.
- [x] Task: validate EvalPlus CLI, benchmark-env imports, SSD output root, and
  generated-solutions JSONL readiness.
- [x] Task: add `scripts/validate_official_coding_preflight.py`.

## Phase 3 - Report And Readiness

- [x] Task: generate
  `reports/benchmark/official-candidates/qwen3-v4-official-coding-preflight-20260616.json`.
- [x] Task: generate
  `reports/benchmark/official-candidates/qwen3-v4-official-coding-preflight-20260616.md`.
- [x] Task: wire the validator into `scripts/validate_readiness.py`.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: EvalPlus and HumanEval are importable in the SSD benchmark
  environment, the queue command now matches the installed EvalPlus interface,
  the output path is SSD-backed, and the current blocker is exactly the absent
  generated-solutions JSONL.
- Remaining gap: official coding scores still require generating solutions for
  HumanEval/MBPP/EvalPlus and then executing the tests.
- Decision: complete this setup track. Do not mark `official-coding` coverage
  present until executed score artifacts are ingested.
