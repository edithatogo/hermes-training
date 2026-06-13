# Specification: mkadrlik Hermes Qwen3.5 9B SFT v7 Qwen No-Think Prefill Completion

## Overview

Close the endpoint-gated `qwen-no-think-prefill` prompt/profile repair row for
`mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` using the already cached GGUF artifact.

## Candidate

- Model: `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`
- Runtime: `llama-server` / GGUF / Metal
- Artifact:
  `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--Hermes-Qwen3.5-9B-SFT-v7/snapshots/bd668b3cfd376d0b961ef43736b5b58ec7978fc0/hermes-qwen3.5-9b-Q4_K_M.gguf`
- Variant: `qwen-no-think-prefill`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`

## Acceptance

- The benchmark must execute against a live local endpoint.
- Results must be recorded with source paths and no promotion claim if strict
  tool-call formatting fails.

## Decision

The candidate scored `0/3`. The prefill exposed valid JSON in one tool case,
but visible `<think>` tags, incomplete parallel calls, and refusal failure keep
raw-output promotion blocked.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: the result is backed by a local endpoint run, source summary, and
  strict no-extra-text BFCL pilot report.
- Remaining gap: use payload normalization, constrained decoding, or a runtime
  wrapper if this lane is revisited.
