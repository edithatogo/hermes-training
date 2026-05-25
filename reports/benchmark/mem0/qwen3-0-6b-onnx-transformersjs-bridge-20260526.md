# Qwen3 0.6B ONNX Transformers.js Bridge Proof

Date: 2026-05-26

## Purpose

Attempt a no-promotion runtime proof for
`onnx-community/Qwen3-Reranker-0.6B-ONNX` through Transformers.js.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_qwen3_onnx_transformersjs_smoke.py \
  --run-id qwen3-0-6b-onnx-transformersjs-cpu-timebox-20260526 \
  --limit-cases 1 \
  --max-length 512 \
  --timeout-s 180
```

## Result

Output:
`/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/qwen3-0-6b-onnx-transformersjs-cpu-timebox-20260526`

| Metric | Value |
|---|---:|
| Status | blocked |
| Exit code | 3 |
| Cases | 0 |
| Top-1 accuracy | 0.000 |
| Rerank latency p50 | 0.000s |

## Blocker

Node and the external SSD Transformers.js tool root are available, and no
repo-local `node_modules` directory was created. The initial default-device
attempt failed because this Transformers.js Node runtime does not support
`wasm`; the CPU retry with `max_length=512` then timed out after `180.0s`
before completing even one fixed-suite case.

The bridge wrapper now accepts `--device coreml` for a later macOS-specific
retry if the installed Transformers.js build exposes that backend. The default
remains `cpu` because it is the portable fail-closed path.

## Decision

Do not promote the ONNX reranker. The Python source-model scorer remains the
only validated Qwen3 0.6B reranker path, and even that remains experimental for
live mem0 because the isolated live fixture favored close-margin reranking.
