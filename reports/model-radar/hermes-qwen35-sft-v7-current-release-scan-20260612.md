# Hermes-Qwen3.5 SFT v7 Current Release Scan

This scan adds the fresh Hermes-Qwen3.5 SFT v7 packs to the Hermes model
radar:

- `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`
- `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7`
- `mkadrlik/hermes-Qwen3.5-2B-SFT-v7`
- `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh`
- `mkadrlik/Hermes-27B-SFT-v7`

## What Changed

- The 9B Hermes-Qwen3.5 pack gives a strong Mac-local runtime comparison lane.
- The 4B, 2B, and 0.8B packs provide useful size-down helper/extractor variants.
- The 27B pack is a higher-capacity teacher/runtime comparison lane.

## Practical Reading

- Treat `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` as the primary local-runtime lane.
- Treat `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` and `mkadrlik/hermes-Qwen3.5-2B-SFT-v7` as comparison lanes.
- Treat `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` as the tiny helper/extractor candidate.
- Treat `mkadrlik/Hermes-27B-SFT-v7` as a teacher/runtime comparison lane.

## Evidence Notes

Verified from current Hugging Face model pages:

- [mkadrlik/Hermes-Qwen3.5-9B-SFT-v7](https://huggingface.co/mkadrlik/Hermes-Qwen3.5-9B-SFT-v7)
- [mkadrlik/Hermes-Qwen3.5-4B-SFT-v7](https://huggingface.co/mkadrlik/Hermes-Qwen3.5-4B-SFT-v7)
- [mkadrlik/hermes-Qwen3.5-2B-SFT-v7](https://huggingface.co/mkadrlik/hermes-Qwen3.5-2B-SFT-v7)
- [mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh](https://huggingface.co/mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh)
- [mkadrlik/Hermes-27B-SFT-v7](https://huggingface.co/mkadrlik/Hermes-27B-SFT-v7)

## Result

The radar now includes a fresh Hermes-specific Qwen3.5 GGUF comparison set
with one primary local-runtime lane and smaller helper variants.
