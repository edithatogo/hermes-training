# Prompt/Profile Repair Selection

- Status: `exhausted`
- Candidate: `None`
- Variant: `None`
- Runner: `none`
- Boundary: A selected repair run is not promotion evidence until raw strict outputs and downstream held-out, pilot, official benchmark, latency, and rollback gates pass.

## Decision

Stop the prompt/profile repair queue. Create a new constrained-decoding, runtime-wrapper, or cloud/offload track before further runs.
