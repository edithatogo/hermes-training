# Unsloth Nemotron 3 Nano 4B GGUF Acquisition Blocked - 2026-06-14

## Summary

`unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF` was checked as priority 2 in the
runtime-proof action queue. The exact package was not present in the SSD-backed
Hugging Face cache, so the first step was to acquire the smallest matching GGUF
artifact before running a llama.cpp strict BFCL endpoint pilot.

The dry-run confirmed a single suitable target:

- `NVIDIA-Nemotron-3-Nano-4B-Q4_K_M.gguf`
- Reported size: `2.9G`

The live download did not make progress: after several polling windows the
cache contained only a zero-byte `.incomplete` blob. The transfer was cancelled
cleanly rather than leaving a hanging process.

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF \
  --include '*Q4_K_M*' \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF \
  NVIDIA-Nemotron-3-Nano-4B-Q4_K_M.gguf \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

## Result

- Dry-run succeeded and reported the `2.9G` Q4_K_M file.
- Live download was cancelled after no bytes landed in the incomplete blob.
- No llama.cpp server was started and no BFCL pilot was run for this exact
  Unsloth package.

## Related Evidence

The official sibling package `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF` is already
runtime-proven and benchmarked locally through llama.cpp:

- `reports/benchmark/local-pilots/nemotron3-nano-4b-q4km-llamacpp-strict-bfcl-pilot-20260613.md`

That sibling strict BFCL pilot scored `0/3`, so the Unsloth package should not
be treated as likely promotion evidence without an exact package proof.

## Decision

- Status: `acquisition-blocked`
- Keep the candidate in the runtime-proof queue.
- Retry acquisition later or use a different transfer path before attempting the
  endpoint pilot.
