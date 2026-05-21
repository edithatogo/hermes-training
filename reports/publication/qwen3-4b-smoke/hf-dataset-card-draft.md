---
license: apache-2.0
task_categories:
- text-generation
language:
- en
tags:
- hermes
- instruction-tuning
- tool-use
- fine-tuning
---

# Hermes Smoke Training Data

## Dataset Details

- Dataset name: `qwen3-4b-smoke` repo-local smoke dataset
- Dataset revision: repo-local smoke splits
- Dataset version: smoke proof only
- License: Apache 2.0 for repo-local artifact; upstream source licenses still need review before any public dataset repo
- Intended use: local smoke training, runtime validation, and publication planning
- Not intended for: public quality claims, production training, or adapter publication without a ready checklist

## Source and Processing

- Source: repo-local Hermes smoke conversations derived from the project training pipeline
- Filters: smoke-only prompt/response curation
- Deduplication method: conversation-hash based preprocessing in the training pipeline
- Split strategy: train / validation / test
- Known exclusions: strict tool-call target examples are not yet audited for dataset publication

## Splits

- Train rows: 462
- Validation rows: 57
- Test rows: 59
- Total rows: 578

## Token Counts

- Train tokens: 2,889 trained tokens
- Validation tokens: not separately reported in the smoke card
- Test tokens: not separately reported in the smoke card
- Total tokens: smoke-scale only
- Token audit method: training-run token count recorded in the run card and benchmark summary

## Validation and Limitations

- Audit command: see the training and benchmark run cards
- Audit result: smoke proof passed, but it is not a publishable dataset release
- Known limitations: too small for quality claims and missing a publish-ready strict tool-call audit
- Missing coverage: strict tool-call target examples and publication audit trail
- Publication blocker: adapter publication remains blocked until the held-out strict local tool-call benchmark passes at `1.000`

## Publication Notes

- Associated model card: [hf-model-card-draft.md](./hf-model-card-draft.md)
- Hugging Face dataset repo: not created
- GitHub commit: pending next hub commit
- Human review status: blocked until `benchmarks/tool_call_local/heldout_suite.json` passes at `1.000`

## Citation

- Repository: `github.com/edithatogo/hermes-training`
- Report: `reports/publication/qwen3-4b-smoke/`
- Contact: repo owner
