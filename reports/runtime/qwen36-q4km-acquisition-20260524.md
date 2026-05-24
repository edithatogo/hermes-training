# Qwen3.6 35B-A3B Q4_K_M Acquisition

Date: 2026-05-24

## Target

- Repository: `Infatoshi/Qwen3.6-35B-A3B-GGUF`
- File: `Qwen3.6-35B-A3B-Q4_K_M.gguf`
- Expected size: `21166757888` bytes
- Destination: `/Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4/Qwen3.6-35B-A3B-Q4_K_M.gguf`

## Current Status

Acquisition is in progress on the external SSD through the resumable ranged downloader.

```bash
tmux attach -t qwen36_download
```

Progress log:

`/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/download-logs/qwen3.6-q4km-ranged-20260524.log`

Chunk state:

`/Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4/Qwen3.6-35B-A3B-Q4_K_M.gguf.parts`

The abandoned aria2 sparse placeholder was removed. Until the final GGUF exists at the expected byte size, this target remains acquisition-only and must not be used as runtime or benchmark evidence.

## Downloader Hardening

The ranged downloader now refreshes the Hugging Face signed URL for each chunk
attempt instead of relying on one long-lived URL. This matters because the
Qwen3.6 GGUF transfer is multi-hour at the observed connection speed.

The active session was restarted after this change and resumed existing chunk
state:

```text
chunks: 316 (12 already complete)
```

The command continues to append progress to the same SSD log path listed above.

## Follow-Up After Completion

1. Confirm final byte size equals `21166757888`.
2. Start llama.cpp with alias `qwen3.6-35b-a3b-q4` on a free local port.
3. Run `ollama-pack/scripts/runtime_smoke.sh` against the OpenAI-compatible endpoint.
4. Run `scripts/run_endpoint_tool_call_benchmark.py` on `benchmarks/tool_call_local/heldout_suite.json` with `/no_think`.
5. Run the endpoint pilot suites and store raw outputs under `/Volumes/PortableSSD/hermes-evals`.
