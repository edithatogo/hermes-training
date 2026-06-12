# Qwen 2507 and Coder-Next Current Release Scan

This scan updates the Qwen lane with the current official releases that are
actually relevant to Hermes workflows:

- `Qwen/Qwen3-4B-Instruct-2507`
- `Qwen/Qwen3-4B-Thinking-2507`
- `Qwen/Qwen3-Coder-Next-GGUF`

## What Changed

- Qwen3-4B now has a current official 2507 instruction release and a separate
  thinking release.
- Qwen3-Coder-Next has an official GGUF tree with Hermes Agent setup guidance in
  the model card.
- The Qwen3.7 guardrail still stands; no official open-weight `Qwen/Qwen3.7-*`
  lane was verified in this refresh.

## Practical Reading

- Treat the Qwen3-4B 2507 models as current hosted or burst-compute comparison
  points.
- Treat Qwen3-Coder-Next-GGUF as the strongest Qwen specialist runtime baseline
  for Hermes-agent workflows.
- Do not promote Qwen3.7 until an official open-weight repo exists.

## Evidence Notes

Verified from current Hugging Face model pages and collections:

- [Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507)
- [Qwen3-4B-Thinking-2507](https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507)
- [Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next)
- [Qwen3-Coder-Next-GGUF](https://huggingface.co/Qwen/Qwen3-Coder-Next-GGUF)

## Result

The radar now includes the latest Qwen releases that are relevant to Hermes
workflows, while keeping Qwen3.7 watchlist-only.
