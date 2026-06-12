# Gemma 4 12B Unsloth Current Release Scan

This scan adds the new Gemma 4 12B packaging lanes to the Hermes model radar:

- `google/gemma-4-12B-it`
- `google/gemma-4-12B`
- `unsloth/gemma-4-12b-it-GGUF`
- `unsloth/gemma-4-12B-it-qat-GGUF`

## What Changed

- Gemma 4 12B now has both the native official release and fresh Unsloth GGUF
  and QAT packaging.
- The Unsloth GGUF lane gives the clearest Mac/Ollama/LM Studio comparison path.
- The QAT GGUF lane is the stricter packaging comparison point for local use.

## Practical Reading

- Treat the Google 12B releases as the native reference point.
- Treat `unsloth/gemma-4-12b-it-GGUF` as the easiest packaging lane.
- Treat `unsloth/gemma-4-12B-it-qat-GGUF` as the stricter packaging lane.

## Evidence Notes

Verified from current Hugging Face model pages:

- [Gemma 4 12B](https://huggingface.co/google/gemma-4-12B)
- [Gemma 4 12B-it](https://huggingface.co/google/gemma-4-12B-it)
- [unsloth/gemma-4-12b-it-GGUF](https://huggingface.co/unsloth/gemma-4-12b-it-GGUF)
- [unsloth/gemma-4-12B-it-qat-GGUF](https://huggingface.co/unsloth/gemma-4-12B-it-qat-GGUF)

## Result

The radar now includes fresh Gemma 4 12B packaging that is better suited to
Mac-local comparison work than the larger 26B/31B lanes.
