# Spec

## Goal

Close the endpoint-gated prompt/profile repair row for
`LGAI-EXAONE/EXAONE-4.0-1.2B` using the already cached GGUF artifact.

## Candidate

- Model: `LGAI-EXAONE/EXAONE-4.0-1.2B`
- Runtime: `llama-server` / GGUF / Metal
- Artifact:
  `/Volumes/PortableSSD/huggingface/hub/models--LGAI-EXAONE--EXAONE-4.0-1.2B-GGUF/snapshots/162446400ea4596377a3ce1d3ddffa32971af0a6/EXAONE-4.0-1.2B-Q4_K_M.gguf`
- Variant: `strict-suffix-copy-exact`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`

## Acceptance

- The benchmark must execute against a live local endpoint.
- Results must be recorded with source paths and no promotion claim if strict
  formatting fails.

## Decision

The candidate scored `0/3`. It ignored available tools, generated prose, and
hallucinated an unavailable deletion function, so strict Hermes raw-output
promotion remains blocked.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: the result is backed by a local endpoint run, source summary, and
  strict no-extra-text BFCL pilot report.
- Remaining gap: no constrained decoding or runtime wrapper was attempted.
