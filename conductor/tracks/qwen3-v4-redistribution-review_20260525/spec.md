# Specification: Qwen3 V4 Dataset Source Redistribution Review

## Overview

The Qwen3 v4 adapter release gate was fail-closed because dataset/source
redistribution review had not been machine-audited. This track reviews every
materialized v4 row source class, records caveats, and clears only the adapter
source-review gate while keeping public dataset publication and public adapter
visibility gated by remaining release requirements.

## Requirements

- Add a source-provenance audit for the materialized v4 strict tool-call rows.
- Record source counts, split counts, no-think variants, unknown sources, and
  source-level redistribution decisions.
- Keep public dataset publication blocked pending human scope approval.
- Update the Qwen3 v4 release decision and checklist without approving public
  Hugging Face publication.
- Keep publication validation fail-closed until standard benchmark positioning,
  finalized model card, and human approval are complete.

## Acceptance Criteria

- `dataset-source-audit.json` exists for the Qwen3 v4 publication bundle.
- `redistribution-review.md` records the review decision and caveats.
- The publication bundle validator requires the new source-review files.
- Readiness validation and unit tests pass.
- Public release remains blocked.

## Out Of Scope

- Publishing the dataset.
- Publishing the adapter publicly.
- Changing Hugging Face repo visibility.
- Retraining the adapter.
