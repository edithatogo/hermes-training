# Nemotron 3 Nano 4B Packaging Current Release Scan

This scan adds the official Nemotron 3 Nano 4B base and fresh local packaging
lanes to the Hermes model radar:

- `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16`
- `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`
- `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF`
- `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit`

## What Changed

- NVIDIA publishes the official 4B BF16 base as the canonical reference.
- NVIDIA publishes an official GGUF packaging lane for local runtime work.
- Unsloth publishes a community GGUF lane that is useful for local comparison.
- mlx-community publishes an Apple-silicon-friendly 4-bit packaging variant.

## Practical Reading

- Treat `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF` as the most direct local
  runtime lane.
- Treat `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF` as the community packaging
  comparison point.
- Treat `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` as the Mac-local
  packaging alternative when MLX is the preferred runtime.

## Evidence Notes

Verified from current Hugging Face model pages:

- [nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16)
- [nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF)
- [unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF](https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF)
- [mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit](https://huggingface.co/mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit)

## Result

The radar now includes a small NVIDIA helper/runtime family with both
official and community local packaging.
