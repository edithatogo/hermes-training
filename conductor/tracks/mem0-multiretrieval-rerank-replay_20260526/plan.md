# Plan: mem0 Multi-Result Rerank Replay Harness

## Phase 1: Replay Harness

- [x] Task: add a replay script that routes fixed-suite cases through the
  live-wrapper rerank abstraction.
- [x] Task: support warm Qwen3 service options and SSD-backed output paths.

## Phase 2: Tests and Benchmarks

- [x] Task: add unit coverage for candidate conversion and metric summaries.
- [x] Task: run heuristic and warm Qwen3 replay benchmarks on a multi-result
  suite.

## Phase 3: Documentation and Gates

- [x] Task: document results, limitations, and next gates.
- [x] Task: update model radar, benchmark index, handoff, and Conductor status.
- [x] Task: run validation and push.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: replay harness created, unit coverage added, validation passed, and warm Qwen3 reached
  top-1 `1.000` on fixed, BGE-derived expanded, and nomic-derived expanded
  suites through the wrapper/service path.
- Gaps: real isolated mem0 add/search fixture proof remains a follow-up.
