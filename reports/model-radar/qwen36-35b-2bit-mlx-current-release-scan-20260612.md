# Qwen3.6 35B 2-bit MLX Current Release Scan

This scan adds the fresh ManiacLabs Qwen3.6 35B 2-bit MLX lane to the Hermes
model radar:

- `ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming`

## What Changed

- ManiacLabs published a fresh 2-bit MLX pack tagged for agentic/tool use.
- The pack is a lower-memory comparison point against the existing 35B-A3B
  teacher and the 27B frontier/runtime lanes.

## Practical Reading

- Treat `ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming` as the primary
  Apple Silicon local-runtime comparison lane.
- Treat `Qwen/Qwen3.6-35B-A3B` as the higher-fidelity teacher reference.
- Treat `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX` and `deepsweet/Qwen3.6-35B-A3B-MLX-oQ4`
  as comparison packaging lanes.

## Evidence Notes

Verified from current Hugging Face model pages:

- [ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming](https://huggingface.co/ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming)

## Result

The radar now includes a new low-memory Qwen3.6 35B local-runtime path for
Apple Silicon comparison work.
