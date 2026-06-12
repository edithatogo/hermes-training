# ByteShape Qwen3.6 35B-A3B MTP IQ4_XS llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`byteshape/Qwen3.6-35B-A3B-MTP-GGUF` was run through the strict Hermes
BFCL-style endpoint pilot using the SSD-backed `IQ4_XS-3.53bpw` GGUF artifact
and Homebrew `llama-server` with MTP speculative decoding enabled.

Result: `0/3` cases passed, pass rate `0.000`.

This is a successful Mac-local MTP runtime proof but a failed strict Hermes
endpoint proof. Unlike the MLX RAM-19GB package, the model produced concise
tool-call-shaped output, but the schemas did not match Hermes' parser contract.

## Artifact

- Repo: `byteshape/Qwen3.6-35B-A3B-MTP-GGUF`
- File: `Qwen3.6-35B-A3B-IQ4_XS-3.53bpw.gguf`
- Local path:
  `/Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-mtp-byteshape-iq4xs/Qwen3.6-35B-A3B-IQ4_XS-3.53bpw.gguf`
- Runtime: Homebrew `llama-server`
- MTP flags: `--spec-type draft-mtp --spec-draft-n-max 4`
- Context: `4096`

## Benchmark

Server:

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-mtp-byteshape-iq4xs/Qwen3.6-35B-A3B-IQ4_XS-3.53bpw.gguf \
  --host 127.0.0.1 \
  --port 18093 \
  --alias byteshape-qwen36-35b-a3b-mtp-iq4xs \
  --ctx-size 4096 \
  --n-gpu-layers 99 \
  --spec-type draft-mtp \
  --spec-draft-n-max 4 \
  --jinja
```

Pilot:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --base-url http://127.0.0.1:18093/v1 \
  --model byteshape-qwen36-35b-a3b-mtp-iq4xs \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id byteshape-qwen36-35b-a3b-mtp-iq4xs-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/byteshape-qwen36-35b-a3b-mtp-iq4xs-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Emitted `<tool_call>` with JSON using `parameters` rather than Hermes `arguments`, producing a parser error. |
| `bfcl-parallel-ticket-routing` | fail | Emitted OpenAI-style `type/function` wrappers and an unterminated multi-call payload, leaving no parseable Hermes tool calls. |
| `bfcl-invalid-tool` | fail | Returned blank output, so it avoided the forbidden tool name but failed the required refusal content. |

## Runtime Notes

- The local Homebrew `llama-server` supports `draft-mtp`; the older external
  llama.cpp build under `/Volumes/PortableSSD/GitHub/llama.cpp` does not list
  `draft-mtp`.
- Server logs confirmed `common_speculative_impl_draft_mtp` initialization.
- Pilot timing showed about `37-40` eval tokens/s and draft acceptance between
  about `0.61` and `0.70`.

## Decision

- Status: `runtime-proven; MTP-proven; strict-endpoint-pilot-complete; not-promoted`
- Do not use as the Hermes default model.
- Keep as a latency/runtime comparison lane and possible format adapter lane.
