# Tiny Helper Standard Benchmark Execution - 2026-06-12

## Summary

This run card records the lightweight benchmark execution slice for the tiny
helper lane.

Lane definition:

- `Qwen/Qwen3.5-0.8B`
- `Qwen/Qwen3.5-2B`
- `openbmb/MiniCPM5-1B-MLX`

Comparison lane:

- `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF`

Artifacts remain on the SSD-backed eval roots:

- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/`
- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/`

## Commands

The local pilot runner is:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --suite benchmarks/endpoint_pilots/<suite>.json \
  --model <model_id> \
  --run-id <run-id> \
  --output-dir /Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/<run-id>
```

Executed subsets in this slice:

- BFCL pilot suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
- IFEval pilot suite: `benchmarks/endpoint_pilots/ifeval_pilot.json`
- Coding pilot suite: `benchmarks/endpoint_pilots/coding_pilot.json`

## Results

| Model | Suite | Run id | Pass rate | Decision |
|---|---|---|---:|---|
| `Qwen/Qwen3.5-0.8B` | BFCL pilot | `qwen35-08b-local-bfcl-pilot-20260612` | `0.000` | blocked |
| `Qwen/Qwen3.5-2B` | BFCL pilot | `qwen35-2b-local-bfcl-pilot-20260612` | `0.000` | blocked |
| `openbmb/MiniCPM5-1B-MLX` | BFCL pilot | `minicpm5-1b-mlx-local-bfcl-pilot-20260612` | `0.000` | blocked |
| `Qwen/Qwen3.5-0.8B` | IFEval pilot | `qwen35-08b-local-ifeval-pilot-20260612` | `0.000` | blocked |
| `Qwen/Qwen3.5-0.8B` | Coding pilot | `qwen35-08b-local-coding-pilot-20260612` | `0.000` | blocked |

## Interpretation

The tiny helper lane remains useful as helper/extraction evidence, not as a
publication-ready Hermes adapter. The models consistently fail strict tool-call
formatting, and the first Qwen helper candidate also fails the lightweight
IFEval and coding pilots.

The current evidence is sufficient to keep the helper lane explicitly marked
as blocked for promotion while preserving the raw outputs for later comparison.
