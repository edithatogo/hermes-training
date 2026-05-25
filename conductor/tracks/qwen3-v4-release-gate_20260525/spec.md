# Specification: Qwen3 V4 Release Evidence And Publication Gate

## Overview

The Qwen3 v4 targeted adapter is the first local Hermes candidate to pass the
strict held-out tool-call gate at `1.000`, and a private Hugging Face draft
adapter has already been uploaded and hash-verified. Public Hugging Face
publication must remain fail-closed until non-quality release gates are
explicitly complete.

This track converts the current release evidence into a machine-checkable gate:
GitHub can carry the evidence bundle now, while public Hugging Face publication
stays blocked unless redistribution review, benchmark positioning, final model
card status, and human approval are all recorded.

## Requirements

- Add a lightweight validator for publication bundles that can distinguish
  blocked/private-draft status from publish-ready status.
- Validate the Qwen3 v4 targeted publication bundle as intentionally blocked
  for public release while preserving the strict local gate evidence.
- Record a clear release decision that explains what is approved, what remains
  blocked, and which exact commands/artifacts support the decision.
- Keep adapter weights, raw benchmark outputs, and generated release artifacts
  out of Git unless they are small reviewed evidence files.
- Preserve the required runtime profile: `/no_think` first user prefix plus
  assistant prefill `<think>\n\n</think>\n\n`.
- Do not make public Hugging Face publication changes or alter repo visibility
  without explicit human approval.

## Acceptance Criteria

- A CLI validator exists and is included in readiness syntax checks.
- Unit tests cover fail-closed checklist parsing and release-gate status.
- The Qwen3 v4 publication bundle has a release decision document.
- The publish-readiness checklist states the machine gate outcome.
- Readiness validation and unit tests pass.
- Conductor registry reflects this track and the final health remains at or
  above `9.5`.

## Out Of Scope

- Public Hugging Face publication.
- Changing private Hugging Face repo visibility.
- Uploading new adapter weights, merged weights, or GGUF artifacts.
- Expanding the training dataset or retraining the adapter.
- Treating pilot benchmark scores as official BFCL, IFEval, or HumanEval
  scores.
