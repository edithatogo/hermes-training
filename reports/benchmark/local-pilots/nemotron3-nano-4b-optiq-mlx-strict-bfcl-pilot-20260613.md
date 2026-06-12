# Nemotron 3 Nano 4B OptiQ MLX Strict BFCL Pilot - 2026-06-13

## Summary

`mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` was run through the
strict Hermes BFCL-style local pilot using the MLX local runner.

Result: `0/3` cases passed, pass rate `0.000`.

The MLX runtime loaded successfully on Apple Silicon, but the generated output
does not satisfy the strict Hermes tool-call contract.

## Artifact

- Repo: `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit`
- Local cache: `/Volumes/PortableSSD/huggingface/hub/models--mlx-community--NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit`
- Runtime: MLX / `mlx_lm`
- Load time reported by runner: `283.1s`

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id nemotron3-nano-4b-optiq-mlx-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/nemotron3-nano-4b-optiq-mlx-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Leaked reasoning, used malformed `<tool_call>`/`</think>` wrappers, fabricated customer data, and repeated `<|im_end|>`. |
| `bfcl-parallel-ticket-routing` | fail | Included reasoning and two malformed tool-call blocks with no closing Hermes-compatible structure, then repeated `<|im_end|>`. |
| `bfcl-invalid-tool` | fail | Refused the unavailable function but repeatedly mentioned `delete_customer_record`, violating the strict exclusion rule. |

## Decision

- Status: `strict-local-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Keep only as MLX runtime comparison evidence against the official GGUF
  Nemotron proof.
