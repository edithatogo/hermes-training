# Conductor Workflow

## Task Workflow

1. Read the relevant track `spec.md`, `plan.md`, and owning repo `CONDUCTOR.md`.
2. Confirm storage with `source scripts/env.sh` for hub-level work or `source ../scripts/env.sh` from nested repos.
3. Run the smallest relevant validation before edits.
4. Make scoped changes in the owning repo.
5. Run validation:
   - hub: `./.venv/bin/python scripts/validate_readiness.py`
   - model tracks: hub readiness plus relevant dry run or smoke run
   - runtime track: syntax checks plus runtime smoke where artifacts exist
6. Update the track plan status and any run notes/docs.
7. Keep generated artifacts ignored unless intentionally published.

## Phase Completion Verification and Checkpointing Protocol

At the end of every phase:

- rerun validation
- update the local track plan
- update `conductor/tracks.md` if track status changes
- summarize remaining blockers
- estimate project/track health using `conductor/health-score.md`
- do not mark a track complete below health 9.5 unless the user explicitly pauses or cancels the track
- only then mark the phase complete

## Commit Policy

Nested repos should be committed before the hub root. The hub should only point to nested repo commits that can be pushed or reproduced.

## Stop Conditions

- validation fails and the fix is not obvious
- a model download requires credentials or license acceptance
- a benchmark would write large artifacts outside SSD-backed paths
- a publishing step would create public artifacts without license confirmation
