# Plan: Runtime-Normalized Tool-Call Report

## Phase 1 - Reporting Tool

- [x] Task: Add a runtime-normalized tool-call scorecard summarizer.
- [x] Task: Validate Python syntax.

## Phase 2 - Evidence And Docs

- [x] Task: Generate a V3 held-out runtime-normalized report on SSD.
- [x] Task: Update runtime and benchmark documentation with report location.
- [x] Task: Run readiness validation.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10.
- Evidence: report generated under `/Volumes/PortableSSD/hermes-evals/runtime-normalized-tool-call/qwen3-4b-strict-toolcall-v3-heldout-20260524/`; repo runtime card records strict `0.250`, runtime-normalized `0.875`, and residual failure `heldout-argument-correctness-lab-order`.
