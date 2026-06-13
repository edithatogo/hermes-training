# Specification: mkadrlik Hermes Qwen3.5 9B SFT v7 Strict-Suffix Completion

## Overview

Close the endpoint-gated `strict-suffix-copy-exact` prompt/profile repair row
for `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` using the already cached GGUF artifact.

## Candidate

- Model: `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`
- Runtime: `llama-server` / GGUF / Metal
- Artifact:
  `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--Hermes-Qwen3.5-9B-SFT-v7/snapshots/bd668b3cfd376d0b961ef43736b5b58ec7978fc0/hermes-qwen3.5-9b-Q4_K_M.gguf`
- Variant: `strict-suffix-copy-exact`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`

## Acceptance

- The benchmark must execute against a live local endpoint.
- Results must be recorded with source paths and no promotion claim if strict
  tool-call formatting fails.

## Decision

The candidate scored `1/3`. It passed only the unavailable-tool refusal case,
so raw-output promotion remains blocked.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: the result is backed by a local endpoint run, source summary, and
  strict no-extra-text BFCL pilot report.
- Remaining gap: payload normalization or constrained decoding would be needed
  before any held-out proof.
