# Plan: mem0 LFM2 Clean-Root Extraction Smoke

## Phase 1: Clean-Root Acquisition

- [x] Task: pull `sam860/LFM2:2.6b` into the clean SSD Ollama root.
- [x] Task: verify `ollama list` shows `sam860/LFM2:2.6b` and
  `nomic-embed-text:latest`.

## Phase 2: Extraction Validation

- [x] Task: run a bounded `/api/generate` smoke for the pulled model.
- [x] Task: run `scripts/run_ollama_memory_extraction_benchmark.py` against
  the smoke suite with outputs on `/Volumes/PortableSSD/hermes-evals`.

## Phase 3: Documentation and Gates

- [x] Task: document the benchmark result and storage/runtime caveats.
- [x] Task: update the mem0 candidate radar, benchmark index, and handoff.
- [x] Task: run repo validation and leave the tree ready to push.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: `sam860/LFM2:2.6b` and `nomic-embed-text:latest` are visible in
  `/Volumes/PortableSSD/Ollama/mem0-clean-models`; bounded generation returned
  exactly `ok`; `extraction-lfm2-2-6b-clean-root-20260526` passed 7/7 cases
  with JSON validity 1.000 and p50 latency 0.874s.
- Gaps: keep this as rollback extraction proof only; broader replacement claims
  still require larger suites or stronger model comparisons.
