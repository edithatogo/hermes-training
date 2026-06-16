# Specification: Qwen3 v4 Official BFCL Preflight

## Overview

Prepare the next missing official-candidate benchmark slice for the promoted
Qwen3 v4 Hermes adapter: BFCL self-hosted generation and evaluation. This track
adds a reproducible preflight and run-card gate, but does not claim benchmark
completion until official BFCL scores exist.

## Goals

- Verify the installed BFCL CLI path under `/Volumes/PortableSSD`.
- Verify the official-candidate queue still marks `official-bfcl` as missing.
- Verify the BFCL command uses `bfcl generate` and `bfcl evaluate` with SSD
  output roots.
- Probe an optional OpenAI-compatible endpoint through `/v1/models`.
- Record a dated preflight report that is explicit about whether BFCL can be
  launched now.
- Wire validation into hub readiness so the preflight cannot silently drift.

## Acceptance Criteria

- Add `scripts/check_official_bfcl_preflight.py` and a matching validator.
- Add unit tests for blocked-endpoint and ready-to-run states.
- Store the generated report under
  `reports/benchmark/official-candidates/`.
- Keep `official-bfcl` marked missing in the official-candidate queue until
  scored BFCL artifacts exist.
- Keep all future BFCL raw outputs under
  `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/`.
- Run focused tests and hub readiness validation.

## Out Of Scope

- Starting a local model endpoint.
- Running `bfcl generate` or `bfcl evaluate` without a reachable endpoint.
- Publishing public benchmark claims.
- Changing the current Hermes default model decision.
