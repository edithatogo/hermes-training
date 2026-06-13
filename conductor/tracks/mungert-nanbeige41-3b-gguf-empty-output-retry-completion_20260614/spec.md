# Specification: Mungert Nanbeige4.1 3B GGUF Empty-Output Retry Completion

## Overview

Close the endpoint-gated `empty-output-retry` prompt/profile repair row for
`Mungert/Nanbeige4.1-3B-GGUF` using the already cached GGUF artifact.

## Candidate

- Model: `Mungert/Nanbeige4.1-3B-GGUF`
- Runtime: `llama-server` / GGUF / Metal
- Artifact:
  `/Volumes/PortableSSD/huggingface/hub/models--Mungert--Nanbeige4.1-3B-GGUF/snapshots/7a35d8054f29ebe6fecc7e54b2b2e313e4307e63/Nanbeige4.1-3B-q4_k_m.gguf`
- Variant: `empty-output-retry`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`

## Acceptance

- The benchmark must execute against a live local endpoint.
- Results must be recorded with source paths and no promotion claim if strict
  tool-call formatting fails.

## Decision

The candidate scored `1/3`. The retry did not improve the strict pass rate, so
raw-output promotion remains blocked.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: the result is backed by a local endpoint run, source summary, and
  strict no-extra-text BFCL pilot report.
- Remaining gap: use constrained decoding or a runtime wrapper if revisited.
