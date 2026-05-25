# Specification: Qwen3 V4 Clean Dataset Materialization

Materialize and audit a cleaned synthetic-only dataset candidate for the Qwen3
v4 adapter without publishing it.

Acceptance criteria:

- Add a reusable materialization script for approved source classes.
- Write generated JSONL data under `/Volumes/PortableSSD`.
- Exclude mirrored seed and seed-derived `/no_think` rows by default.
- Re-run source, overlap, and token audits against the cleaned dataset.
- Record a dated report and keep public dataset publication blocked.
- Validation passes.
