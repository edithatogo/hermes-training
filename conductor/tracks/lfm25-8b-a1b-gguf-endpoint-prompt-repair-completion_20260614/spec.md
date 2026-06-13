# Specification: LFM2.5 8B A1B GGUF Endpoint Prompt Repair Completion

## Overview

Close the endpoint-gated prompt/profile repair row for
`LiquidAI/LFM2.5-8B-A1B-GGUF` using the already cached GGUF artifact.

## Candidate

- Model: `LiquidAI/LFM2.5-8B-A1B-GGUF`
- Runtime: `llama-server` / GGUF / Metal
- Artifact:
  `/Volumes/PortableSSD/huggingface/hub/models--LiquidAI--LFM2.5-8B-A1B-GGUF/snapshots/dfd5fdcad7a1c0d31473fb4ca443b8befbacddf0/LFM2.5-8B-A1B-Q4_K_M.gguf`
- Variant: `strict-suffix-copy-exact`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`

## Acceptance

- The benchmark must execute against a live local endpoint.
- Results must be recorded with source paths and no promotion claim if strict
  tool-call formatting fails.

## Decision

The candidate scored `0/3`. It did not emit Hermes tool calls for available
tools and mentioned the forbidden delete tool in the refusal case, so raw-output
promotion remains blocked.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: the result is backed by a local endpoint run, source summary, and
  strict no-extra-text BFCL pilot report.
- Remaining gap: no constrained decoding or runtime wrapper was attempted.
