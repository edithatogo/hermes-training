# North Mini Code GGUF Q4_K_M Smoke

Run ID: `north-mini-code-gguf-q4km-smoke-20260612`
Started: 2026-06-11T15:17:59Z
Model: `CohereLabs/North-Mini-Code-1.0`
GGUF repo: `unsloth/North-Mini-Code-1.0-GGUF`
GGUF file: `North-Mini-Code-1.0-UD-Q4_K_M.gguf`
Runtime: Homebrew `llama-cli` version 9290
Output log: `/Volumes/PortableSSD/hermes-evals/runtime-format-lanes/gguf-portability/north-mini-code-gguf-q4km-smoke-20260612/llama-cli.log`
HF cache: `/Volumes/PortableSSD/huggingface/hub/models--unsloth--North-Mini-Code-1.0-GGUF`

## Result

| Check | Result |
|---|---|
| SSD-backed artifact acquisition | Passed |
| Artifact cache size | 18G |
| `llama-cli` model load | Failed |
| Exit code | 1 |
| Wall time | 1856.55s |
| Maximum resident set size | 108560384 bytes |
| Peak memory footprint | 71566008 bytes |

## Failure

Current Homebrew `llama.cpp` cannot load this GGUF because it does not recognize
the model architecture:

```text
llama_model_load: error loading model: unknown model architecture: 'cohere2moe'
llama_model_load_from_file_impl: failed to load model
common_init_from_params: failed to load model '/Volumes/PortableSSD/huggingface/hub/models--unsloth--North-Mini-Code-1.0-GGUF/snapshots/e306bb4bf0df610f5471d97a01de2b6e0b24d356/North-Mini-Code-1.0-UD-Q4_K_M.gguf'
```

The same log also notes that `--no-conversation` is no longer supported by
`llama-cli` and recommends `llama-completion`, but the blocking issue occurs
before generation because the runtime cannot parse `cohere2moe`.

## Decision

This is a completed blocked runtime proof. The artifact now exists on the
external SSD, but North Mini Code is not a usable local GGUF runtime target for
Hermes until the runtime supports `cohere2moe` or an alternative compatible
runner is selected. No quality, coding, or Hermes tool-use benchmark claim is
made from this run.

Next acceptable proof paths:

- retry with a `llama.cpp` build that explicitly supports `cohere2moe`;
- test through LM Studio only if its bundled runtime can load the same GGUF;
- test through a Transformers/safetensors path if the 30B/3B-active MoE fits
  the selected local or cloud environment;
- keep this as a code-specialist watchlist model until one of those runtime
  paths passes a bounded smoke.
