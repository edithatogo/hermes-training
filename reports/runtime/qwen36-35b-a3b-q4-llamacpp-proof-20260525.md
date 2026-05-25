# Qwen3.6 35B-A3B Q4_K_M llama.cpp Runtime Proof

Date: 2026-05-25

## Target

- Model: `Qwen3.6-35B-A3B-Q4_K_M`
- Runtime alias: `qwen3.6-35b-a3b-q4`
- Artifact: `/Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4/Qwen3.6-35B-A3B-Q4_K_M.gguf`
- Expected size: `21166757888` bytes
- Actual size: `21166757888` bytes
- Runtime: `/Volumes/PortableSSD/GitHub/llama.cpp/build/bin/llama-server`
- Endpoint used: `http://127.0.0.1:8093/v1`

## Smoke

The watcher `scripts/watch_qwen36_q4_runtime_proof.sh` detected the exact-size
GGUF and ran `scripts/run_qwen36_q4_runtime_proof.sh`.

Result:

- `/v1/models`: passed
- `/v1/chat/completions`: passed
- Chat latency: `12440ms`
- Smoke output: `/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/qwen36-35b-a3b-q4-llamacpp-20260524/smoke.txt`
- Run summary: `/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/qwen36-35b-a3b-q4-llamacpp-20260524/summary.txt`

## Benchmarks

| Suite | Cases | Pass Rate |
|---|---:|---:|
| Held-out strict tool-call | 8 | `0.000` |
| BFCL-style pilot | 3 | `0.000` |
| IFEval-style pilot | 3 | `0.000` |
| Coding sanity pilot | 3 | `0.333` |

Raw outputs:

- Held-out: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-tool-call-benchmark/qwen3.6-35b-a3b-q4-llamacpp-heldout-nothink-20260524`
- BFCL pilot: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3.6-35b-a3b-q4-bfcl-pilot-nothink-20260524`
- IFEval pilot: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3.6-35b-a3b-q4-ifeval-pilot-nothink-20260524`
- Coding pilot: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3.6-35b-a3b-q4-coding-pilot-nothink-20260524`

## Cleanup

The redundant ranged-download chunk directory was removed after exact-size
assembly and runtime proof:

`/Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4/Qwen3.6-35B-A3B-Q4_K_M.gguf.parts`

The retained artifact root is approximately `20G`.

## Decision

This is a valid Mac-local GGUF runtime proof, not a publishable Hermes-agent
improvement. Qwen3.6 Q4_K_M loads and serves through llama.cpp, but the strict
tool-call gate failed completely. Keep it as frontier runtime evidence and a
comparison baseline. Do not publish model-improvement claims from this run.
