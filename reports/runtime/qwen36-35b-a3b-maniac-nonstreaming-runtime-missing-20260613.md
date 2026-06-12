# Qwen3.6 35B-A3B Maniac Nonstreaming Runtime Missing - 2026-06-13

## Summary

`ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming` was checked as the next
Qwen3.6 35B-A3B local-runtime candidate in the Hermes proof queue.

The package is not a plain `mlx_lm` model. Its model card states that it runs
through the Maniac engine using `lme-serve`, while GGUF users should use the
sibling `ManiacLabs/Qwen3.6-35B-A3B-2bit` repo.

The local machine does not currently have `lme-serve` or a `maniac` command
available, so no resident Maniac-engine benchmark was run.

## Artifact

- Repo: `ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming`
- Size: about `13.5G` total repository payload
- Runtime specified by model card:
  - `lme-serve ./qwen3.6-35b-2bit-resident --no-streaming`
  - optional `--target-only` to disable speculative decoding
- Recommended hardware from model card: `24 GB+` Apple Silicon for fully
  resident serving

## Local Runtime Check

```bash
command -v lme-serve
command -v maniac
ls -la /Applications | rg -i 'maniac|lme'
```

Result: no local Maniac runtime was found.

## Decision

- Status: `specialist-runtime-blocked`
- Do not download the 13.5G nonstreaming Maniac-engine package until
  `lme-serve` or the Maniac app is installed.
- For immediate Mac-local Hermes comparison, use the sibling GGUF package
  `ManiacLabs/Qwen3.6-35B-A3B-2bit` through `llama.cpp` or LM Studio instead.
