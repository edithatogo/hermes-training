# Specification: North-Mini-Code GGUF Packaging Refresh

## Overview

Capture the fresh `unsloth/North-Mini-Code-1.0-GGUF` lane that appeared in the
live Hugging Face refresh and keep it visible as a code-agent comparison point
for Hermes workflows.

## Scope

- Add `unsloth/North-Mini-Code-1.0-GGUF` to the machine-readable radar.
- Mark the lane as runtime-blocked until `cohere2moe` support is available in
  the local executor stack.
- Update the current release scan and project docs so the packaging lane is
  discoverable.

## Out Of Scope

- No runtime proof in this slice.
- No training or benchmark claims.
- No publication or adapter promotion.

## Acceptance Criteria

- The candidate list contains the new GGUF lane with the correct status.
- The release scan mentions the packaging-only addition and the runtime block.
- The handoff and roadmap docs reflect the new lane.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.5 / 10`
- Evidence: the new lane is source-backed and relevant to Hermes agent runtime
  selection, even though it is not yet runnable locally.
- Remaining gap: runtime proof is intentionally out of scope.
