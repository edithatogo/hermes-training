# LFM2 24B-A2B Q4_K_M Acquisition

Date: 2026-05-25

## Target

- Repository: `LiquidAI/LFM2-24B-A2B-GGUF`
- File: `LFM2-24B-A2B-Q4_K_M.gguf`
- Expected size: `14415473952` bytes
- Destination: `/Volumes/PortableSSD/hermes-models/frontier-gguf/lfm2-24b-a2b-q4/LFM2-24B-A2B-Q4_K_M.gguf`

## Final Status

Acquisition completed on the external SSD through the resumable ranged
downloader. The final GGUF exists at the expected byte size and the runtime
proof completed.

```bash
tmux attach -t lfm2_24b_download
```

Progress log:

`/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/download-logs/lfm2-24b-a2b-q4-ranged-20260525.log`

Chunk state:

`/Volumes/PortableSSD/hermes-models/frontier-gguf/lfm2-24b-a2b-q4/LFM2-24B-A2B-Q4_K_M.gguf.parts`

Initial state:

```text
chunks: 215 (0 already complete)
expected size: 14415473952 bytes
active session: lfm2_24b_download
```

First live checkpoint:

```text
chunks complete: 0 / 215
active temp chunks: 16
partial root size: 126M
active session: lfm2_24b_download
```

Latest live checkpoint:

```text
chunks complete: 160 / 215
active temp chunks: 16
partial root size: 11G
active session: lfm2_24b_download
```

Session health checkpoint:

```text
checked: 2026-05-25T22:15:01+1000
chunks complete: 163 / 215
active temp chunks: 16
partial root size: 11G
observed rate: ~1.15 MiB/s
final GGUF: not assembled
download session: lfm2_24b_download active
proof watcher: lfm2_24b_proof_watch active
remaining: 52 chunks before final assembly and exact-size proof
```

Later live checkpoint:

```text
checked: 2026-05-25T22:34:34+1000
chunks complete: 181 / 215
active temp chunks: 16
final GGUF: not assembled
remaining: 34 chunks before final assembly and exact-size proof
```

Current live checkpoint:

```text
checked: 2026-05-25T22:45:45+1000
chunks complete: 194 / 215
active temp chunks: 16
partial bytes complete: 13019119616
final GGUF: not assembled
remaining: 21 chunks before final assembly and exact-size proof
observed rate: ~1.14 MiB/s
```

Completion checkpoint:

```text
checked: 2026-05-25T23:01:47+1000
chunks complete before assembly: 215 / 215
final GGUF size: 14415473952 bytes
runtime smoke: passed
strict held-out pass: 0.375
BFCL-style pilot: 0.333
IFEval-style pilot: 1.000
Coding sanity pilot: 1.000
runtime proof report: reports/runtime/lfm2-24b-a2b-q4-llamacpp-proof-20260525.md
redundant parts directory: removed after proof
```

## Post-Download Proof

An SSD-backed watcher is active:

```bash
tmux attach -t lfm2_24b_proof_watch
```

Watcher log:

`/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/logs/lfm2-24b-a2b-q4-proof-watch-20260525.log`

The watcher detected the final GGUF at the exact expected byte size, then ran:

```bash
bash scripts/run_lfm2_24b_q4_runtime_proof.sh
```

The helper started llama.cpp with alias `lfm2-24b-a2b-q4`, ran a runtime smoke,
ran the held-out strict tool-call suite with `/no_think`, ran the endpoint
pilot suites, and stored raw outputs under `/Volumes/PortableSSD/hermes-evals`.

## Boundary

This target is no longer acquisition-only. It is runtime-proven, but its strict
Hermes-agent tool-call score is below promotion threshold.
