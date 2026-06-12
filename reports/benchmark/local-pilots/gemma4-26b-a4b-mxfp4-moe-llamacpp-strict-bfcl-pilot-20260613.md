# Gemma 4 26B-A4B MXFP4_MOE llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`unsloth/gemma-4-26B-A4B-it-GGUF` was run through the strict Hermes
BFCL-style endpoint pilot using the SSD-backed `MXFP4_MOE` GGUF artifact and
Homebrew `llama-server`.

Strict BFCL result: `2/3` cases passed, pass rate `0.667`.

Expanded pilot result on the same local artifact:

- Coding pilot: `3/3`, pass rate `1.000`.
- IFEval pilot: `3/3`, pass rate `1.000`.

This is the strongest frontier local proof in the current Qwen3.6/Gemma 4
comparison slice. It is runtime-proven on the M1 Max, produced exact Hermes
tool-call syntax for both BFCL tool-call cases, and passed the small coding and
instruction-following pilots. It is not promoted to default yet because the
strict invalid-tool refusal case failed and the evidence is still pilot-scale.

## Artifact

- Repo: `unsloth/gemma-4-26B-A4B-it-GGUF`
- File: `gemma-4-26B-A4B-it-MXFP4_MOE.gguf`
- Local path:
  `/Volumes/PortableSSD/hermes-models/frontier-gguf/gemma-4-26b-a4b-unsloth-mxfp4-moe/gemma-4-26B-A4B-it-MXFP4_MOE.gguf`
- Runtime: Homebrew `llama-server`
- Context: `4096`

## Benchmark

Server:

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/hermes-models/frontier-gguf/gemma-4-26b-a4b-unsloth-mxfp4-moe/gemma-4-26B-A4B-it-MXFP4_MOE.gguf \
  --host 127.0.0.1 \
  --port 18094 \
  --alias gemma4-26b-a4b-mxfp4-moe \
  --ctx-size 4096 \
  --n-gpu-layers 99 \
  --jinja
```

Pilot:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --base-url http://127.0.0.1:18094/v1 \
  --model gemma4-26b-a4b-mxfp4-moe \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id gemma4-26b-a4b-mxfp4-moe-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/gemma4-26b-a4b-mxfp4-moe-llamacpp-strict-bfcl-pilot-20260613`

## Result

### BFCL Pilot

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | pass | Exact single Hermes `<tool_call>` with `name` and `arguments`; no extra text. |
| `bfcl-parallel-ticket-routing` | pass | Exact two-call Hermes `<tool_call>` sequence; no extra text. |
| `bfcl-invalid-tool` | fail | Correctly refused, but repeated the unavailable forbidden delete tool name and missed the strict refusal wording check. |

### Coding Pilot

Run ID: `gemma4-26b-a4b-mxfp4-moe-llamacpp-coding-pilot-20260613`

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/gemma4-26b-a4b-mxfp4-moe-llamacpp-coding-pilot-20260613`

| Case | Result | Note |
|---|---:|---|
| `coding-python-add-two` | pass | Returned only the requested `add_two` function. |
| `coding-python-filter-even` | pass | Returned only the requested `evens` function. |
| `coding-sql-basic` | pass | Returned a valid SQL query with the required fields and ordering. |

### IFEval Pilot

Run ID: `gemma4-26b-a4b-mxfp4-moe-llamacpp-ifeval-pilot-20260613`

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/gemma4-26b-a4b-mxfp4-moe-llamacpp-ifeval-pilot-20260613`

| Case | Result | Note |
|---|---:|---|
| `ifeval-json-only-invoice` | pass | Returned exact parseable JSON. |
| `ifeval-bullets-count` | pass | Returned exactly three bullet lines. |
| `ifeval-forbidden-word` | pass | Avoided the forbidden word and returned the required phrase. |

## Runtime Notes

- llama.cpp emitted Gemma control-token warnings during load, but the model
  loaded successfully and produced valid tool-call syntax.
- Server logs showed about `50` eval tokens/s on the BFCL pilot cases and about
  `30-48` eval tokens/s during the concurrent coding and IFEval pilots.
- The local prompt template was detected as `peg-gemma4`.

## Decision

- Status: `runtime-proven; strict-endpoint-pilot-complete; not-default-yet`
- Keep as the best frontier Gemma local comparison lane.
- Next useful proof is a broader BFCL run and a refusal-format prompt profile to
  check whether the remaining failure can be fixed without fine-tuning.
