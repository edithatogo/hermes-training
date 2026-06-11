# LFM2.5 8B A1B Q4_K_M llama.cpp Smoke - 2026-06-12

## Summary

`LiquidAI/LFM2.5-8B-A1B-GGUF` was acquired to the SSD-backed Hugging Face cache
and load-proven through Homebrew llama.cpp build 9290 on the Mac lane.

This is runtime evidence only. The bounded prompt did not produce compliant
Hermes-style JSON, so the model is not promoted for Hermes tool-calling or
adapter work.

## Artifact

- Repo: `LiquidAI/LFM2.5-8B-A1B-GGUF`
- File: `LFM2.5-8B-A1B-Q4_K_M.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--LiquidAI--LFM2.5-8B-A1B-GGUF/snapshots/dfd5fdcad7a1c0d31473fb4ca443b8befbacddf0/LFM2.5-8B-A1B-Q4_K_M.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Acquisition note: initial Hugging Face request returned HTTP 429 and then
  completed after client backoff.

## Runtime

- Binary: `/opt/homebrew/bin/llama-completion`
- Version: `9290 (bcfd1989e)`
- Build: AppleClang for Darwin arm64

## Command

```bash
/opt/homebrew/bin/llama-completion \
  -m /Volumes/PortableSSD/huggingface/hub/models--LiquidAI--LFM2.5-8B-A1B-GGUF/snapshots/dfd5fdcad7a1c0d31473fb4ca443b8befbacddf0/LFM2.5-8B-A1B-Q4_K_M.gguf \
  --ctx-size 512 \
  --n-predict 8 \
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
  "wall_time_s": 1.652,
  "max_rss_kb": 5287952384,
  "stdout_tail": " {\"data\": {\"items\": [{\"id\\n\\n"
}
```

Runtime metrics from llama.cpp stderr:

- Load time: `707.68 ms`
- Prompt eval: `231.43 tokens/s`
- Generation eval: `109.59 tokens/s`
- Total generation work: `110.97 ms / 17 tokens`

## Failed Attempt Notes

`llama-cli` auto-enabled conversation mode from the model template. A bounded
8-token run with `--no-conversation --single-turn --simple-io` exited quickly,
but printed:

```text
--no-conversation is not supported by llama-cli
please use llama-completion instead
```

The earlier default `llama-cli` bounded run timed out after `180s` while
emitting repeated interactive prompts, so `llama-completion` is the correct
batch proof path for this artifact.

## Decision

- Status: `completed-runtime-proof; hermes-smoke-blocked`
- Do not promote to Hermes default, training, or publication.
- Next gate: run a stricter prompt profile or OpenAI-compatible endpoint smoke
  only if this model is needed as an 8B LFM comparison baseline.
