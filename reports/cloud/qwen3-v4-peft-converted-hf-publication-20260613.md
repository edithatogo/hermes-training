# Qwen3 V4 PEFT Converted Adapter Hub Publication

Status: `published`

Public repository:

```text
https://huggingface.co/edithatogo/qwen3-4b-hermes-lora-peft-converted
```

## Purpose

The converted PEFT package gives persistent cloud jobs a Hub-mounted adapter
artifact. The original public adapter repo, `edithatogo/qwen3-4b-hermes-lora`,
contains the MLX-style adapter (`adapters.safetensors`). The new repo contains
the converted PEFT artifact (`adapter_model.safetensors`) for CUDA/Hugging Face
tooling.

## Upload Record

| Item | Value |
| --- | --- |
| Repo type | model |
| Visibility | public |
| Metadata commit | `6446d8c5256ffe21669b478e1e8f4d55646e1f7e` |
| Weights commit | `97c969fdcc92e7b25eb79f57e12d87a5da1761ee` |
| Local source | `/Volumes/PortableSSD/hermes-evals/adapters/qwen3-v4-peft-conversion-20260613` |
| Upload note | `HF_HUB_DISABLE_XET=1` was required for the weights upload; the default Xet upload path stalled before commit. |

Remote files verified:

- `.gitattributes`
- `README.md`
- `adapter_config.json`
- `adapter_model.safetensors`
- `conversion-manifest.json`
- `conversion-report.json`

## Local Hashes

| File | SHA256 |
| --- | --- |
| `adapter_model.safetensors` | `bc7a57e38798388297cb77ec4bc6d90bc9e96cc0be74c438dfe1a3a11305928a` |
| `adapter_config.json` | `cddc1256b7ff47185a755e8f527a7e2b065cfb42bc5bb90bd4f86c913f721fd1` |
| `conversion-manifest.json` | `5ba233f163d36bfebd7b889603178aaf74983f730f36a7e177a5a033670792ef` |
| `conversion-report.json` | `9a5fbf5049f3b7d8d9de89c4bb0d4fa5c5101a171117f6ffd4287c0e0a93e8f3` |
| `README.md` | updated before upload to identify the PEFT conversion route |

## Claim Boundary

This is an experimental format conversion, not a new training run. The PEFT
route has passed static PEFT load, Colab T4 load smoke, and a bounded
selected-task `lm_eval[hf]` route pilot. Full no-limit benchmark coverage is
still blocked until a persistent backend completes all selected tasks.
