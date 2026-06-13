# Spec

## Goal

Close the endpoint-gated prompt/profile repair row for
`google/gemma-4-E2B-it-qat-q4_0-gguf` using the already cached GGUF artifact.

## Candidate

- Model: `google/gemma-4-E2B-it-qat-q4_0-gguf`
- Runtime: `llama-server` / GGUF / Metal
- Artifact:
  `/Volumes/PortableSSD/huggingface/hub/models--google--gemma-4-E2B-it-qat-q4_0-gguf/snapshots/1894d1fc0a19d86697abd40483f5983c867df03f/gemma-4-E2B_q4_0-it.gguf`
- Variant: `strict-suffix-copy-exact`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`

## Acceptance

- The benchmark must execute against a live local endpoint.
- Results must be recorded with source paths and no promotion claim if strict
  tool-call formatting fails.

## Decision

The candidate scored `1/3`, passing only the invalid-tool refusal. The tool-call
cases used malformed payloads and failed strict Hermes parsing, so raw-output
promotion remains blocked.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: the result is backed by a local endpoint run, source summary, and
  strict no-extra-text BFCL pilot report.
- Remaining gap: no constrained decoding or runtime wrapper was attempted.
