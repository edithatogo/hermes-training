# Specification: Handoff and Roadmap Reconciliation

Update project-level handoff and roadmap documentation after the current pushed
state changed materially:

- Qwen3 v4 is the public/recommended strict tool-call adapter.
- Qwen3 v5 is a documented negative experiment and must not replace v4.
- `ollama-pack` runtime packaging track is complete.
- Nested repos are clean and pushed at current submodule pointers.
- SSD-backed paths are canonical for this workspace.

Acceptance criteria:

- `HANDOFF.md` reflects `/Volumes/PortableSSD/GitHub/hermes-training` as the
  canonical working root.
- `HANDOFF.md` current state and next actions match the current publication and
  runtime status.
- `PARALLEL_ROADMAP.md` no longer presents completed lanes as still merely
  started.
- `REPO_MAINTENANCE.md` no longer lists stale dirty nested-repo state as
  current.
- Validation passes after the documentation update.
