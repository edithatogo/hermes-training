# Gemma 4 26B-A4B Profiled Endpoint Held-Out Tool-Call Benchmark - 2026-06-13

## Summary

`unsloth/gemma-4-26B-A4B-it-GGUF` was run through the full local held-out
Hermes tool-call suite using the same SSD-backed `MXFP4_MOE` GGUF artifact,
Homebrew `llama-server`, and the `gemma4-26b-refusal-system-suffix` runtime
profile that repaired the strict BFCL pilot.

Result: `7/8` strict cases passed, pass rate `0.875`.

The profile remains the best currently validated Gemma 4 runtime profile because
it preserves JSON validity, repairs invalid-tool refusal behavior, and passes
both held-out multi-turn repair cases. It is not yet a publication/default gate
pass because one held-out argument-correctness case failed by expanding a
free-text argument rather than copying the expected phrase exactly.

## Artifact

- Repo: `unsloth/gemma-4-26B-A4B-it-GGUF`
- File: `gemma-4-26B-A4B-it-MXFP4_MOE.gguf`
- Local path:
  `/Volumes/PortableSSD/hermes-models/frontier-gguf/gemma-4-26b-a4b-unsloth-mxfp4-moe/gemma-4-26B-A4B-it-MXFP4_MOE.gguf`
- Runtime: Homebrew `llama-server`
- Context: `4096`
- Prompt profile: `gemma4-26b-refusal-system-suffix`

## Command

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

Benchmark:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_tool_call_benchmark.py \
  --base-url http://127.0.0.1:18094/v1 \
  --model gemma4-26b-a4b-mxfp4-moe \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --run-id gemma4-26b-a4b-mxfp4-moe-profile-heldout-toolcall-20260613 \
  --max-tokens 512 \
  --timeout-s 240 \
  --system-suffix " If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Do not repeat unavailable tool names."
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/gemma4-26b-a4b-mxfp4-moe-profile-heldout-toolcall-20260613`

## Result

| Metric | Result |
|---|---:|
| Cases | `8` |
| Passed | `7` |
| Pass rate | `0.875` |
| JSON validity rate | `1.000` |
| Argument correctness rate | `0.833` |
| Invalid-tool handling rate | `1.000` |
| Multi-turn repair rate | `1.000` |
| Empty-think wrapper cases | `0` |

Failure:

- `heldout-argument-correctness-lab-order`: strict JSON was valid and tool names
  were correct, but `notify_care_team.arguments.message` was expanded to
  `The lab order for CBC, CMP, and ferritin is ready for review.` instead of the
  expected copied phrase `order is ready for review`.

## Profile Tradeoff Check

A stricter v2 suffix was also tested:

```text
If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Do not repeat unavailable tool names. For valid tool calls, copy identifiers, enum-like strings, dates, emails, and user-provided free-text argument values exactly from the user; do not expand, paraphrase, or add detail.
```

Run ID:
`gemma4-26b-a4b-mxfp4-moe-profile-v2-heldout-toolcall-20260613`

SSD output:

`/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/gemma4-26b-a4b-mxfp4-moe-profile-v2-heldout-toolcall-20260613`

Result: `7/8` pass rate, but JSON validity fell to `0.833`. The failed
lab-order case changed to a non-Hermes `function` / `parameters` schema and
omitted the second tool call. Reject this v2 profile.

## Decision

- Status:
  `runtime-proven; profile-repaired-pilot-complete; heldout-toolcall-0.875; not-default-yet`
- Keep `gemma4-26b-refusal-system-suffix` as the active Gemma 4 runtime profile.
- Do not promote Gemma 4 26B-A4B as the Hermes default until the remaining
  free-text argument-copying failure is fixed by fine-tuning, adapter repair, or
  a less brittle but predeclared benchmark contract.
