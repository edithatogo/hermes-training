# Plan: Qwen3 V4 Clean Dataset Materialization

## Phase 1: Script

- [x] Task: add `scripts/materialize_publication_dataset.py`.
- [x] Task: add unit coverage for source filtering and validation split naming.
- [x] Task: include the script in structural readiness syntax checks.

## Phase 2: Materialization And Audits

- [x] Task: materialize the cleaned synthetic-only dataset to SSD.
- [x] Task: run source audit, overlap audit, and token audit.
- [x] Task: record the report and generated artifact paths.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: generated data is SSD-backed, seed sources are excluded, audits are
  recorded, and validation passes.
- Gaps: no public dataset repo was created; explicit human approval remains
  required before release.
- Decision: complete as a local materialized candidate, not a publication.
