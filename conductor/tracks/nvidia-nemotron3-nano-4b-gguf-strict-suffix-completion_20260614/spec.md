# Specification: NVIDIA Nemotron 3 Nano 4B GGUF Strict-Suffix Completion

## Overview

Close the endpoint-gated `strict-suffix-copy-exact` prompt/profile repair row
for `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`.

## Candidate

- Model: `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`
- Runtime: `llama-server` / GGUF / Metal
- Artifact:
  `/Volumes/PortableSSD/huggingface/hub/models--nvidia--NVIDIA-Nemotron-3-Nano-4B-GGUF/snapshots/ba223d14e45525f7fae81db77ea8cabeb2fc6c25/NVIDIA-Nemotron3-Nano-4B-Q4_K_M.gguf`
- Variant: `strict-suffix-copy-exact`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`

## Decision

The candidate scored `1/3`. It passed only the unavailable-tool refusal case,
so raw-output promotion remains blocked.
