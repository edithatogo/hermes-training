# LFM2 24B-A2B Q4_K_M llama.cpp Runtime Proof

Date: 2026-05-25

## Identity

- Model alias: `lfm2-24b-a2b-q4`
- Source repository: `LiquidAI/LFM2-24B-A2B-GGUF`
- Artifact: `/Volumes/PortableSSD/hermes-models/frontier-gguf/lfm2-24b-a2b-q4/LFM2-24B-A2B-Q4_K_M.gguf`
- Exact size: `14415473952` bytes
- Runtime: `/Volumes/PortableSSD/GitHub/llama.cpp/build/bin/llama-server`
- Endpoint used during proof: `http://127.0.0.1:8095/v1`
- Context size: `4096`

## Proof Trigger

The SSD-backed watcher detected the exact-size final GGUF and ran:

```bash
bash scripts/run_lfm2_24b_q4_runtime_proof.sh
```

Watcher log:

```text
/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/logs/lfm2-24b-a2b-q4-proof-watch-20260525.log
```

Runtime proof root:

```text
/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/lfm2-24b-a2b-q4-llamacpp-20260524
```

The run ID kept the helper's previous default `20260524` date stamp. The helper
has since been fixed to default future runs to the current date.

## Runtime Smoke

Result: passed.

Smoke output:

```text
/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/lfm2-24b-a2b-q4-llamacpp-20260524/smoke.txt
```

The proof server was stopped after capture to release unified memory.

## Benchmark Results

| Suite | Result | Raw output root |
|---|---:|---|
| Strict held-out Hermes tool-call | `0.375` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-tool-call-benchmark/lfm2-24b-a2b-q4-llamacpp-heldout-nothink-20260524` |
| BFCL-style pilot | `0.333` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/lfm2-24b-a2b-q4-bfcl-pilot-nothink-20260524` |
| IFEval-style pilot | `1.000` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/lfm2-24b-a2b-q4-ifeval-pilot-nothink-20260524` |
| Coding sanity pilot | `1.000` | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/lfm2-24b-a2b-q4-coding-pilot-nothink-20260524` |

Held-out diagnostics:

- JSON validity: `0.500`
- Argument accuracy: `0.333`
- Invalid-tool handling: `0.500`
- Multi-turn repair: `1.000`
- Empty-think prefix cases: `0`
- Residual strict failures: `5 / 8`

## Storage Cleanup

After exact-size assembly and proof, the redundant ranged chunk directory was
removed:

```text
/Volumes/PortableSSD/hermes-models/frontier-gguf/lfm2-24b-a2b-q4/LFM2-24B-A2B-Q4_K_M.gguf.parts
```

This reclaimed approximately `13G`; the final GGUF remains on the external SSD.

## Decision

LFM2 24B-A2B Q4_K_M is now runtime-proven locally through llama.cpp and useful
as a frontier LFM comparison runtime. It is not a Hermes-agent publication
candidate without additional tool-call alignment work because the strict
held-out gate is below threshold.
