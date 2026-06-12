# Roadmap Regression and Publication Gate

## Overview

Maintain consistency between `FUTURE_MODELS.md`, `MODEL_CANDIDATES.yaml`, the completed scan report, benchmark evidence, and `HANDOFF.md` as execution tracks produce new results. This is the repo hygiene and publication-safety lane for the model roadmap.

## Scope

- Detect drift between roadmap prose, candidate metadata, scan reports, benchmark reports, runtime proof queues, and handoff notes.
- Preserve publication gates for datasets, model adapters, and public benchmark claims.
- Keep cloud/offload evidence separate from local reproducibility evidence.
- Ensure all generated artifacts are either intentionally tracked or ignored.
- Keep track registry state accurate after execution phases complete.

## Out of Scope

- Running heavy model benchmarks directly; this track validates and reconciles their outputs.
- Publishing Hugging Face or GitHub artifacts without explicit approval.
- Editing historical reports to erase failed evidence.
- Marking execution tracks complete solely because docs were updated.

## Acceptance Criteria

- Roadmap and candidate metadata agree on active, blocked, rejected, promoted, and watchlist candidates.
- Handoff notes identify the next execution lane and current blockers.
- Publication gates clearly distinguish local-only, private, restricted, and public-safe artifacts.
- Readiness and candidate consistency checks pass before commit.
- Remote GitHub state includes the completed reconciliation.

## Health Target

This track should not be marked complete below health 9.5. Completion requires a clean repository state and a pushed commit unless explicitly paused.
