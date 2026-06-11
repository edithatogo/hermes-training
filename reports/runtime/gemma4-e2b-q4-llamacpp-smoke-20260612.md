# Gemma 4 E2B QAT q4_0 llama.cpp Smoke - 2026-06-12

## Summary

`google/gemma-4-E2B-it-qat-q4_0-gguf` was acquired to the SSD-backed Hugging
Face cache and load-proven through Homebrew llama.cpp build 9290.

This is runtime evidence only. The bounded text prompt exited successfully but
returned only end-of-text, so the model is not promoted for Hermes JSON,
tool-calling, training, or publication.

## Artifact

- Repo: `google/gemma-4-E2B-it-qat-q4_0-gguf`
- File: `gemma-4-E2B_q4_0-it.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--google--gemma-4-E2B-it-qat-q4_0-gguf/snapshots/1894d1fc0a19d86697abd40483f5983c867df03f/gemma-4-E2B_q4_0-it.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Multimodal projector: not downloaded for this text-only smoke.

## Runtime

- Binary: `/opt/homebrew/bin/llama-completion`
- Version: `9290 (bcfd1989e)`
- Build: AppleClang for Darwin arm64

## Command

```bash
/opt/homebrew/bin/llama-completion \
  -m /Volumes/PortableSSD/huggingface/hub/models--google--gemma-4-E2B-it-qat-q4_0-gguf/snapshots/1894d1fc0a19d86697abd40483f5983c867df03f/gemma-4-E2B_q4_0-it.gguf \
  --ctx-size 512 \
  --n-predict 16 \
  --temp 0 \
  --seed 1 \
  --no-display-prompt \
  --no-conversation \
  --simple-io \
  --prompt 'Return only JSON: {"ok": true}'
```

## Result

```json
{
  "timed_out": false,
  "returncode": 0,
  "wall_time_s": 2.703,
  "max_rss_kb": 3531030528,
  "stdout_tail": " [end of text]\\n\\n\\n"
}
```

Runtime metrics from llama.cpp stderr:

- Load time: `937.79 ms`
- Prompt eval: `74.93 tokens/s`
- Total generation work: `134.35 ms / 11 tokens`
- Max RSS from wrapper: about `3.53 GB`

Runtime warnings:

- llama.cpp overrode control-looking token types for `<|tool_response>` and
  `</s>`.
- llama.cpp removed `</s>` from the EOG list because
  `special_eog_ids` contained `<|tool_response>`.

## Decision

- Status: `completed-runtime-proof; empty-output-blocked`
- Do not promote to Hermes default, training, or publication.
- Next gate: use a model-specific chat template/profile or MLX package before
  any BFCL/Hermes benchmark attempt.
