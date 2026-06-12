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

| Model | Suite | Run id | Avg latency | Avg words | Empty rate | Decision |
|---|---|---|---:|---:|---:|---|
| `Qwen/Qwen3.5-0.8B` | BFCL pilot | `qwen35-08b-local-bfcl-pilot-20260612` | n/a | n/a | n/a | blocked |
| `Qwen/Qwen3.5-2B` | BFCL pilot | `qwen35-2b-local-bfcl-pilot-20260612` | n/a | n/a | n/a | blocked |
| `openbmb/MiniCPM5-1B-MLX` | BFCL pilot | `minicpm5-1b-mlx-local-bfcl-pilot-20260612` | n/a | n/a | n/a | blocked |
| `Qwen/Qwen3.5-0.8B` | IFEval pilot | `qwen35-08b-local-ifeval-pilot-20260612` | n/a | n/a | n/a | blocked |
| `Qwen/Qwen3.5-0.8B` | Coding pilot | `qwen35-08b-local-coding-pilot-20260612` | n/a | n/a | n/a | blocked |
| `Qwen/Qwen3.5-0.8B` | Hermes-local 100 | `qwen35-08b-expanded-hermes-local-20260612` | `1.47s` | `78.09` | `0.000` | pass |
| `Qwen/Qwen3.5-2B` | Hermes-local 100 | `qwen35-2b-expanded-hermes-local-20260612` | `2.32s` | `78.57` | `0.000` | pass |
| `openbmb/MiniCPM5-1B-MLX` | Hermes-local 100 | `minicpm5-1b-expanded-hermes-local-20260612` | `0.54s` | `74.30` | `0.060` | pass with empty-rate caveat |

## Interpretation

The tiny helper lane remains useful as helper/extraction evidence, not as a
publication-ready Hermes adapter. The models still fail strict tool-call
formatting, but the 100-prompt Hermes-local pass is now recorded for all three
candidate models. MiniCPM5 still shows a non-zero empty-response rate on the
expanded set, so it remains a weaker helper/extraction comparison point.

The current evidence is sufficient to keep the helper lane explicitly marked
as blocked for promotion while preserving the raw outputs for later comparison.
