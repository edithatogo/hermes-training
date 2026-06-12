# Gemma 4 26B-A4B MXFP4_MOE llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`unsloth/gemma-4-26B-A4B-it-GGUF` was run through the strict Hermes
BFCL-style endpoint pilot using the SSD-backed `MXFP4_MOE` GGUF artifact and
Homebrew `llama-server`.

Strict BFCL result: `2/3` cases passed, pass rate `0.667`.

Expanded pilot result on the same local artifact:

- Coding pilot: `3/3`, pass rate `1.000`.
- IFEval pilot: `3/3`, pass rate `1.000`.
- BFCL with `gemma4-26b-refusal-system-suffix` profile and `max_tokens=512`:
  `3/3`, pass rate `1.000`.
- Full held-out local Hermes tool-call suite with the same profile:
  `7/8`, pass rate `0.875`.

This is the strongest frontier local proof in the current Qwen3.6/Gemma 4
comparison slice. It is runtime-proven on the M1 Max, produced exact Hermes
tool-call syntax for both BFCL tool-call cases, and passed the small coding and
instruction-following pilots. A system-suffix runtime profile also repaired the
strict invalid-tool refusal case. It is not promoted to default yet because the
held-out evidence still has one strict argument-copying failure and broader
BFCL/safety/coding coverage is still required.

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

Raw strict BFCL pilot:

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

Profiled strict BFCL pilot:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --base-url http://127.0.0.1:18094/v1 \
  --model gemma4-26b-a4b-mxfp4-moe \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id gemma4-26b-a4b-mxfp4-moe-llamacpp-system-refusal-profile-512-bfcl-pilot-20260613 \
  --max-tokens 512 \
  --require-no-extra-tool-text \
  --system-suffix " If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Do not repeat unavailable tool names."
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

### BFCL With Refusal System Profile

Run ID: `gemma4-26b-a4b-mxfp4-moe-llamacpp-system-refusal-profile-512-bfcl-pilot-20260613`

Profile: `gemma4-26b-refusal-system-suffix`

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/gemma4-26b-a4b-mxfp4-moe-llamacpp-system-refusal-profile-512-bfcl-pilot-20260613`

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | pass | Exact single Hermes `<tool_call>` with `name` and `arguments`; no extra text. |
| `bfcl-parallel-ticket-routing` | pass | Exact two-call Hermes `<tool_call>` sequence; no extra text. |
| `bfcl-invalid-tool` | pass | Returned the required refusal without repeating the unavailable tool name. |

Profile tradeoff checks:

- User-prefix profile v1/v2 fixed invalid-tool refusal but caused the parallel
  tool-call case to return blank.
- System-suffix profile with `max_tokens=256` fixed invalid-tool refusal but
  truncated the parallel tool-call payload.
- System-suffix profile with `max_tokens=512` passed all three strict BFCL pilot
  cases.

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

### Held-Out Local Tool-Call Suite

Run ID: `gemma4-26b-a4b-mxfp4-moe-profile-heldout-toolcall-20260613`

Profile: `gemma4-26b-refusal-system-suffix`

SSD output:

`/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/gemma4-26b-a4b-mxfp4-moe-profile-heldout-toolcall-20260613`

Report:

`reports/benchmark/endpoint-tool-call/gemma4-26b-a4b-mxfp4-moe-profile-heldout-toolcall-20260613.md`

| Metric | Result |
|---|---:|
| Cases | `8` |
| Passed | `7` |
| Pass rate | `0.875` |
| JSON validity rate | `1.000` |
| Argument correctness rate | `0.833` |
| Invalid-tool handling rate | `1.000` |
| Multi-turn repair rate | `1.000` |

The single strict failure was `heldout-argument-correctness-lab-order`: Gemma
produced valid Hermes tool-call JSON and correct tool names, but expanded the
free-text `message` argument instead of copying the expected phrase exactly. A
stricter v2 suffix was tested and rejected because it kept the pass rate at
`0.875` while lowering JSON validity to `0.833`.

## Runtime Notes

- llama.cpp emitted Gemma control-token warnings during load, but the model
  loaded successfully and produced valid tool-call syntax.
- Server logs showed about `50` eval tokens/s on the BFCL pilot cases and about
  `30-48` eval tokens/s during the concurrent coding and IFEval pilots.
- The local prompt template was detected as `peg-gemma4`.
- The strict 3/3 repair requires the `gemma4-26b-refusal-system-suffix` profile
  and `max_tokens=512`.

## Decision

- Status:
  `runtime-proven; profile-repaired-strict-pilot-complete; heldout-toolcall-0.875; not-default-yet`
- Keep as the best frontier Gemma local comparison lane.
- Next useful proof is a tool-call fine-tune or runtime-adapter repair for exact
  free-text argument copying, followed by a repeated held-out gate and broader
  BFCL/safety/coding benchmark pass using the profile.
