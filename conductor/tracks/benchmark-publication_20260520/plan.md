# Plan: Benchmark and Publication Hardening

## Phase 1: Benchmark Structure

- [x] Task: Document Hermes-local benchmark gates.
- [x] Task: Document standard benchmark suites and when to run them.
- [x] Task: Add dataset token audit script.
- [x] Task: Move benchmark caches and outputs to SSD-backed environment paths.
- [x] Task: Conductor - Automated Review and Checkpoint 'Benchmark Structure' (Protocol in workflow.md)

## Phase 2: Publication Documentation

- [x] Task: Document model card and dataset card requirements.
- [x] Task: Document benchmark artifact publication options.
- [x] Task: Add reusable run-card template.
- [x] Task: Add reusable Hugging Face model-card template.
- [x] Task: Add populated Qwen3 smoke run-card and HF model-card draft with score provenance.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Documentation' (Protocol in workflow.md)

## Phase 3: Benchmark Execution

- [x] Task: Expand Hermes-local eval set to 100+ prompts.
- [x] Task: Run base vs LFM2.5 smoke adapter evaluation.
- [x] Task: Run base vs Qwen3 smoke adapter evaluation.
- [x] Task: Add standard benchmark smoke commands for `lm-evaluation-harness`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Benchmark Execution' (Protocol in workflow.md)

## Health Check

- [x] Task: Estimate track health using hub `conductor/health-score.md`.
- Current estimate: 9.7 / 10
- Evidence: run-card and Hugging Face model-card templates exist, the `lm-evaluation-harness` smoke command template exists, both local eval files contain 100 prompts with required category coverage, LFM2.5 base vs full-smoke adapter evaluation is summarized in `lfm2/eval/lfm25-full-smoke-summary.md`, Qwen3 base vs smoke adapter evaluation is summarized in `gemma4/eval/qwen3-4b-smoke-summary.md`, populated Qwen3 publication drafts live in `reports/publication/qwen3-4b-smoke/`, and `./.venv/bin/python scripts/validate_readiness.py` passes.
- Gaps: standard benchmarks remain planned rather than executed for the smoke adapter; this is documented as a release blocker and should not prevent closing the scaffold/hardening track.
- Next action: run the standard benchmark suite only for a non-smoke candidate adapter, then replace the draft HF card with release-grade results.
- [x] Task: Close or document all gaps below health 9.5.
- [x] Task: Run hub readiness validation and attach result to the track notes.
- [x] Task: Confirm health >= 9.5 before marking this track complete.
