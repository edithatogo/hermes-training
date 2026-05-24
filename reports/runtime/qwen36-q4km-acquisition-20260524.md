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

Most recent live check on 2026-05-24 shows the transfer continuing:

```text
chunks complete: 115 / 316
partial root size: 8.2G
active session: qwen36_download
```

An SSD-backed watcher is now available so the runtime proof can start
automatically as soon as the final GGUF is assembled:

```bash
tmux new-session -d -s qwen36_proof_watch \
  "cd /Volumes/PortableSSD/GitHub/hermes-training && POLL_SECONDS=300 bash scripts/watch_qwen36_q4_runtime_proof.sh"
```

Watcher log:

`/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/logs/qwen3.6-q4km-proof-watch-20260524.log`

## Follow-Up After Completion

1. Confirm final byte size equals `21166757888`.
2. Run the post-download proof helper:

```bash
source scripts/env.sh
bash scripts/run_qwen36_q4_runtime_proof.sh
```

The helper starts llama.cpp with alias `qwen3.6-35b-a3b-q4`, runs the runtime
smoke, runs the held-out strict tool-call suite with `/no_think`, runs the
endpoint pilot suites, and stores raw outputs under `/Volumes/PortableSSD/hermes-evals`.
