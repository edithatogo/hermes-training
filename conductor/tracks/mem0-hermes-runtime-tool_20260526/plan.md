# Plan: mem0 Hermes Runtime Tool

## Phase 1: Tool Contract

- [x] Task: add `scripts/hermes_mem0_tool.py`.
- [x] Task: add a checked-in Hermes-agent tool manifest.
- [x] Task: document command and stdin JSON usage.

## Phase 2: Validation

- [x] Task: add unit coverage for payload parsing, argument mapping, output
  rendering, and error output.
- [x] Task: run a live tool smoke against local mem0.
- [x] Task: record the smoke evidence.

## Phase 3: Completion

- [x] Task: update handoff and mem0 docs.
- [x] Task: run full unit/readiness/publication gates.
- [x] Task: mark the track complete and push.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: wrapper tests pass; live command smoke returned `ok: true`,
  read-only, first-read latency `3.999s`, and second-read cache-hit latency
  `0.000s`.
- Gaps: Hermes-agent repo wiring remains a separate plugin/install step because
  that checkout is behind upstream and has local edits.
