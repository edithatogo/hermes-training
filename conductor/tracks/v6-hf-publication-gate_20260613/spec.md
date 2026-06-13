# Qwen3 v6 Hugging Face Adapter Publication Gate

## Overview

The Qwen3 4B strict tool-call v6 adapter has a validated local promotion and a
prepared Hugging Face dry-run package, but public publication must remain
blocked until model-card, benchmark-scope, and human-approval gates are
explicitly satisfied. This track adds a fail-closed publication path that can
validate the package now and perform an upload later only when all approval
evidence is present.

## Functional Requirements

- Provide a hub-level command that validates a prepared HF adapter package
  before any upload action.
- Require adapter files, model card, package manifest, SSD-backed package
  location, and target repo consistency.
- Print the exact human approval phrase required for a later publication.
- Refuse upload unless `--publish` is explicitly passed and an approval file
  contains the exact phrase.
- Preserve current v6 blockers; a dry-run package must not silently become a
  public release.
- Keep GitHub publication separate from Hugging Face publication.

## Non-Functional Requirements

- No large artifacts are written to Git.
- Package and export paths stay under `/Volumes/PortableSSD` by default.
- The command is scriptable and emits JSON for CI/Conductor checks.
- Hub readiness must include syntax validation for the publication command.

## Acceptance Criteria

- `scripts/publish_hf_adapter_package.py` validates the v6 package in dry-run
  mode and reports remaining blockers.
- `scripts/publish_hf_adapter_package.py --publish` fails without exact human
  approval evidence.
- `scripts/validate_readiness.py` passes.
- The track plan records evidence and a health score of at least `9.5 / 10`.

## Out Of Scope

- Actual Hugging Face upload.
- Marking v6 public-release gates complete.
- Broadening official benchmark coverage beyond the already recorded IFEval
  pilot.
- Mutating live Hermes or mem0 defaults.
