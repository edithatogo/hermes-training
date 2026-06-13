# Qwen3 V4 PEFT Colab Load Smoke

Date: 2026-06-13

Status: `scored`

## Runtime

| Field | Value |
|---|---|
| Colab accelerator | `gpu:T4` |
| CUDA device | `Tesla T4` |
| Python | `3.12.13` |
| Torch | `2.11.0+cu128` |
| Raw log | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-load-smoke-20260613/colab-exec.log` |
| JSON result | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-load-smoke-20260613/qwen3-v4-peft-load-smoke.json` |

## Artifact

| Field | Value |
|---|---|
| Uploaded tarball | `/content/qwen3-v4-peft-conversion-20260613.tar.gz` |
| Remote adapter dir | `/content/qwen3-v4-peft-conversion-20260613` |
| Base model | `Qwen/Qwen3-4B` |
| PEFT base model | `Qwen/Qwen3-4B` |

## Result

| Field | Value |
|---|---:|
| Dependency install latency | 7.144s |
| 4-bit base + PEFT load latency | 115.904s |
| Generation latency | 4.234s |

Sample output from the minimal prompt:

```text
No other keys or values. Also, the JSON should be in a single line, no line breaks. Also, the
```

## Decision

The converted PEFT candidate loads on Colab T4 with `Qwen/Qwen3-4B` through
Transformers, PEFT, and bitsandbytes 4-bit quantization. This is a load smoke
only, not a quality benchmark. It is sufficient to create a follow-on Colab
selected-task `lm-eval` execution track for the converted PEFT candidate.
