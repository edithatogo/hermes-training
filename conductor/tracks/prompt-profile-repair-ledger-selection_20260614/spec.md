# Specification: Prompt/Profile Repair Ledger And Selection

## Overview

The repair queue and experiment matrix define what could be run, but execution
still needs a fail-closed ledger that separates local, endpoint-gated, and
non-local rows. This track adds that ledger and keeps the existing dry-run
selection helper as the single-command handoff for one-at-a-time repair work.

## Goals

- Keep all 18 prompt/profile repair candidates visible in an execution ledger.
- Exclude non-local/cloud-only rows from executable Mac-local experiment
  commands.
- Separate pending local, pending endpoint, analysis-variant, and blocked
  statuses.
- Preserve a dry-run selected experiment without executing benchmarks.
- Validate ledger freshness and readiness.

## Acceptance Criteria

- `reports/benchmark/coverage/prompt-profile-repair-ledger-20260614.*` exists
  and is deterministic.
- Non-local rows have `blocked-non-local` status and no executable experiments.
- Pending rows have explicit promotion gates and blank `result_report` fields.
- The selected default dry-run remains non-executing and strict.
- Focused tests, ledger validator, selection validator, Conductor consistency,
  and full readiness pass.

## Out Of Scope

- Running any repair benchmark.
- Starting endpoint services.
- Downloading model artifacts.
- Promoting any model or prompt profile.
