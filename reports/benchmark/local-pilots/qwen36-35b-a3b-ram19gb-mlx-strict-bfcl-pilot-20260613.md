# Qwen3.6 35B-A3B RAM-19GB MLX Strict BFCL Pilot - 2026-06-13

## Summary

`baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX` was run through the strict Hermes
BFCL-style local pilot using the MLX local runner.

Result: `0/3` cases passed, pass rate `0.000`.

This is a successful Mac-local runtime proof but a failed strict Hermes
endpoint proof. The model loaded and generated on the M1 Max from the
SSD-backed Hugging Face cache, but its raw completions are not compatible with
the current Hermes tool-call parser without fine-tuning, a prompt/profile
adapter, or a strict output normalizer.

## Artifact

- Repo: `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX`
- Local cache: `/Volumes/PortableSSD/huggingface/hub/models--baa-ai--Qwen3.6-35B-A3B-RAM-19GB-MLX`
- Cache size after acquisition: about `19G`
- Runtime: MLX
- Load time reported by runner: `1900.9s`

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id qwen36-35b-a3b-ram19gb-mlx-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen36-35b-a3b-ram19gb-mlx-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Leaked planning text and emitted a malformed `<tool_call>` fragment with an unexpected `</think>` marker, leaving no parseable tool call. |
| `bfcl-parallel-ticket-routing` | fail | Leaked reasoning text and emitted an unterminated JSON-style tool-call list, leaving no parseable Hermes tool calls. |
| `bfcl-invalid-tool` | fail | Correctly reasoned that the requested tool was unavailable, but still mentioned the forbidden delete tool name, failing the strict exclusion check. |

## Decision

- Status: `runtime-proven; strict-endpoint-pilot-complete; not-promoted`
- Do not use as the Hermes default model.
- Keep as a Qwen3.6 MoE comparison point and possible adapter/fine-tuning lane
  because it fits the Mac-local runtime target but currently fails strict
  Hermes tool-call formatting.
