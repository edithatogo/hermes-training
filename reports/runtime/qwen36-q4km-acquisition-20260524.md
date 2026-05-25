# Qwen3.6 35B-A3B Q4_K_M Acquisition

Date: 2026-05-24

## Target

- Repository: `Infatoshi/Qwen3.6-35B-A3B-GGUF`
- File: `Qwen3.6-35B-A3B-Q4_K_M.gguf`
- Expected size: `21166757888` bytes
- Destination: `/Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4/Qwen3.6-35B-A3B-Q4_K_M.gguf`

## Current Status

Acquisition completed on 2026-05-25. The final GGUF exists at the expected
byte size and has been runtime-proven through llama.cpp.

Progress log:

`/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/download-logs/qwen3.6-q4km-ranged-20260524.log`

Chunk state:

`/Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4/Qwen3.6-35B-A3B-Q4_K_M.gguf.parts`

The abandoned aria2 sparse placeholder was removed. The redundant ranged
download chunk directory was also removed after exact-size assembly and runtime
proof to recover SSD space.

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
After increasing concurrency to 32 workers, the observed state was:

```text
chunks complete: 21 / 316
partial root size: 1.8G
active session: qwen36_download
```

The transfer is still acquisition-only. Do not use the partial `.parts`
directory as runtime evidence.

Later live check on 2026-05-24 confirmed the downloader was still making
byte-level progress:

```text
chunks complete: 49 / 316
active temp chunks: 32
partial root size: 4.0G
active session: qwen36_download
```

Final state:

```text
final size: 21166757888 bytes
artifact root size after chunk cleanup: 20G
runtime proof: reports/runtime/qwen36-35b-a3b-q4-llamacpp-proof-20260525.md
```

The SSD-backed watcher ran the runtime proof automatically after exact-size
assembly:

```bash
tmux new-session -d -s qwen36_proof_watch \
  "cd /Volumes/PortableSSD/GitHub/hermes-training && POLL_SECONDS=300 bash scripts/watch_qwen36_q4_runtime_proof.sh"
```

Watcher log:

`/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/logs/qwen3.6-q4km-proof-watch-20260524.log`

## Runtime Proof Result

- Smoke: passed
- Held-out strict tool-call pass: `0.000`
- BFCL-style pilot: `0.000`
- IFEval-style pilot: `0.000`
- Coding sanity pilot: `0.333`

Decision: runtime proof only. This artifact is useful as a frontier local
runtime baseline, but it is not promotion-ready for Hermes-agent tool use.
