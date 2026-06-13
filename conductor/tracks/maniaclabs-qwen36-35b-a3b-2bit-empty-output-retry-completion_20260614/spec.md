# Specification: ManiacLabs Qwen3.6 35B A3B 2bit Empty-Output Retry Completion

## Overview

Close the endpoint-gated `empty-output-retry` prompt/profile repair row for
`ManiacLabs/Qwen3.6-35B-A3B-2bit` using the already cached GGUF artifact.

## Candidate

- Model: `ManiacLabs/Qwen3.6-35B-A3B-2bit`
- Runtime: `llama-server` / GGUF / Metal
- Artifact:
  `/Volumes/PortableSSD/huggingface/hub/models--ManiacLabs--Qwen3.6-35B-A3B-2bit/snapshots/5f92fade67bd6712b339fad950f86296d1b0a71e/qwen3.6-35b-a3b-iq2xxs-q2k.gguf`
- Variant: `empty-output-retry`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`

## Acceptance

- The benchmark must execute against a live local endpoint.
- Results must be recorded with source paths and no promotion claim if strict
  tool-call formatting fails.

## Decision

The candidate scored `2/3`. It passed the parallel tool-call case and the
unavailable-tool refusal, but the single lookup case retained a malformed
closing tag, so raw-output promotion remains blocked.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: the result is backed by a local endpoint run, source summary, and
  strict no-extra-text BFCL pilot report.
- Remaining gap: no held-out proof, constrained decoding, or runtime wrapper
  was attempted.
